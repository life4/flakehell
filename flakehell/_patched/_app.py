# built-in
import sys
from argparse import ArgumentParser
from itertools import chain
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# external
from flake8.main.application import Application
from flake8.options.config import MergedConfigParser, get_local_plugins
from flake8.plugins.manager import ReportFormatters
from flake8.utils import parse_unified_diff

# app
from .._constants import DEFAULTS
from .._logic import read_config
from ._checkers import FlakeHellCheckersManager
from ._plugins import FlakeHellCheckers
from ._style_guide import FlakeHellStyleGuideManager


# Options that are related to the flake8 codes management logic.
# We use our own codes management via `plugins` and `exceptions`.
UNSUPPORTED = frozenset({
    '--extend-exclude',     # use only `exclude` in the config
    '--per-file-ignores',   # use `exceptions`
    '--statistics',         # use `--format=stat` instead

    '--ignore',             # use `plugins`
    '--extend-ignore',      # use `plugins`
    '--select',             # use `plugins`
    '--enable-extensions',  # use `plugins`
})


class FlakeHellApplication(Application):
    """
    Reloaded flake8 original entrypoint to provide support for some features:
    + pyproject.toml support
    + replace CheckersManager to support for `plugins` option
    + register custom formatters
    """
    guide: FlakeHellStyleGuideManager

    @property
    def option_manager(self):
        """We overload this property only to specify setter.
        """
        return self._option_manager

    @option_manager.setter
    def option_manager(self, manager):
        """Hook to add flakehell options into flake8 options parser.
        """
        group = manager.parser.add_argument_group('FlakeHell')
        group.add_argument('--baseline', help='path to baseline')
        group.add_argument('--safe', action='store_true', help='suppress exceptions from plugins')
        self._option_manager = manager

    def get_toml_config(self, path: Path = None) -> Dict[str, Any]:
        if path is not None:
            return read_config(path)
        # lookup for config from current dir up to root
        root = Path().resolve()
        for dir_path in chain([root], root.parents):
            path = dir_path / 'pyproject.toml'
            if path.exists():
                return read_config(path)
        return dict()

    @staticmethod
    def extract_toml_config_path(argv: List[str]) -> Tuple[Optional[Path], List[str]]:
        if not argv:
            return None, argv

        if '--help' in argv:
            argv = argv.copy()
            argv.remove('--help')
            if not argv:
                return None, ['--help']

        parser = ArgumentParser()
        parser.add_argument('--config')
        known, unknown = parser.parse_known_args(argv)
        if known.config and known.config.endswith('.toml'):
            return Path(known.config).expanduser(), unknown
        return None, argv

    def parse_configuration_and_cli(self, config_finder, argv: List[str]) -> None:
        parser = self.option_manager.parser
        for action in parser._actions.copy():
            if not action.option_strings:
                continue
            name = action.option_strings[-1]
            if name not in UNSUPPORTED:
                continue
            parser._handle_conflict_resolve(None, [(name, action)])

        # if passed `--config` with path to TOML-config, we should extract it
        # before passing into flake8 mechanisms
        config_path, argv = self.extract_toml_config_path(argv=argv)

        # make default config
        config, _ = self.option_manager.parse_args([])
        config.__dict__.update(DEFAULTS)

        # patch config wtih TOML
        # If config is explicilty passed, it will be used
        # If config isn't specified, flakehell will lookup for it
        config.__dict__.update(self.get_toml_config(config_path))

        # Parse CLI options and legacy flake8 configs.
        # Based on `aggregate_options`.
        config_parser = MergedConfigParser(
            option_manager=self.option_manager,
            config_finder=config_finder,
        )
        parsed_config = config_parser.parse()
        config.extended_default_select = self.option_manager.extended_default_select.copy()
        for config_name, value in parsed_config.items():
            dest_name = config_name
            # If the config name is somehow different from the destination name,
            # fetch the destination name from our Option
            if not hasattr(config, config_name):
                dest_name = config_parser.config_options[config_name].dest
            setattr(config, dest_name, value)
        self.options, self.args = self.option_manager.parse_args(
            args=argv,
            values=config,
        )

        # All this goes from the original `parse_configuration_and_cli`.
        # We can't call `super` anymore because all `Application` methods
        # redefine everything.
        self.running_against_diff = self.options.diff
        if self.running_against_diff:
            self.parsed_diff = parse_unified_diff()
            if not self.parsed_diff:
                self.exit()
        self.options._running_from_vcs = False
        self.check_plugins.provide_options(
            optmanager=self.option_manager,
            options=self.options,
            extra_args=self.args,
        )
        self.formatting_plugins.provide_options(
            optmanager=self.option_manager,
            options=self.options,
            extra_args=self.args,
        )

    def make_file_checker_manager(self) -> None:
        self.file_checker_manager = FlakeHellCheckersManager(
            baseline=self.options.baseline,
            style_guide=self.guide,
            arguments=self.args,
            checker_plugins=self.check_plugins,
        )

    def find_plugins(self, config_finder) -> None:
        local_plugins = get_local_plugins(config_finder)
        sys.path.extend(local_plugins.paths)
        self.check_plugins = FlakeHellCheckers(local_plugins.extension)  # this line is changed
        self.formatting_plugins = ReportFormatters(local_plugins.report)
        self.check_plugins.load_plugins()
        self.formatting_plugins.load_plugins()

    def make_formatter(self, *args, **kwargs) -> None:
        if self.formatter is None:
            super().make_formatter(*args, **kwargs)

    def make_guide(self) -> None:
        """Patched StyleGuide creation just to use FlakeHellStyleGuideManager
        instead of original one.
        """
        if self.guide is None:
            self.guide = FlakeHellStyleGuideManager(self.options, self.formatter)

        if self.running_against_diff:
            self.guide.add_diff_ranges(self.parsed_diff)
