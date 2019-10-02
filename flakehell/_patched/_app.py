import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from flake8.main.application import Application
from flake8.options.aggregator import aggregate_options
from flake8.options.config import get_local_plugins

from ._checkers import FlakeHellCheckersManager
from ._style_guide import FlakeHellStyleGuideManager
from .._constants import DEFAULTS
from .._logic import read_config
from ._plugins import FlakeHellCheckers


class FlakeHellApplication(Application):
    """
    Reloaded flake8 original entrypoint to provide support for some features:
    + pyproject.toml support
    + replace CheckersManager to support for `plugins` option
    + register custom formatters
    """

    def get_toml_config(self, path: Path = None) -> Dict[str, Any]:
        if path is not None:
            return read_config(path)
        # lookup for config from current dir up to root
        for dir_path in Path('lol').parents:
            path = dir_path / 'pyproject.toml'
            if path.exists():
                return read_config(path)
        return dict()

    @staticmethod
    def extract_toml_config_path(argv: List[str] = None) -> Tuple[Optional[Path], Optional[List[str]]]:
        if not argv:
            return None, argv
        parser = ArgumentParser()
        parser.add_argument('--config')
        known, unknown = parser.parse_known_args(argv)
        if known.config and known.config.endswith('.toml'):
            return Path(known.config).expanduser(), unknown
        return None, argv

    def parse_configuration_and_cli(self, argv: List[str] = None) -> None:
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

        # parse CLI options and legacy flake8 configs
        self.options, self.args = aggregate_options(
            manager=self.option_manager,
            config_finder=self.config_finder,
            arglist=argv,
            values=config,
        )
        super().parse_configuration_and_cli(argv=argv)

    def make_file_checker_manager(self) -> None:
        self.file_checker_manager = FlakeHellCheckersManager(
            baseline=getattr(self.options, 'baseline', None),
            style_guide=self.guide,
            arguments=self.args,
            checker_plugins=self.check_plugins,
        )

    def find_plugins(self) -> None:
        if self.local_plugins is None:
            self.local_plugins = get_local_plugins(
                self.config_finder,
                self.prelim_opts.config,
                self.prelim_opts.isolated,
            )

        sys.path.extend(self.local_plugins.paths)

        if self.check_plugins is None:
            self.check_plugins = FlakeHellCheckers(self.local_plugins.extension)
        super().find_plugins()

    def make_guide(self) -> None:
        """Patched StyleGuide creation just to use FlakeHellStyleGuideManager
        instead of original one.
        """
        if self.guide is None:
            self.guide = FlakeHellStyleGuideManager(self.options, self.formatter)

        if self.running_against_diff:
            self.guide.add_diff_ranges(self.parsed_diff)
