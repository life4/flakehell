from pathlib import Path
from typing import Dict, Any, List

from entrypoints import EntryPoint
from flake8.main.application import Application
from flake8.plugins.manager import Plugin
from flake8.options.aggregator import aggregate_options

from ._checkers import FlakeHellCheckersManager
from ._style_guide import FlakeHellStyleGuideManager
from ..formatters import FORMATTERS
from .._constants import NAME, DEFAULTS
from .._logic import read_config


class FlakeHellApplication(Application):
    """
    Reloaded flake8 original entrypoint to provide support for some features:
    + pyproject.toml support
    + replace CheckersManager to support for `plugins` option
    + register custom formatters
    """

    def get_toml_config(self) -> Dict[str, Any]:
        path = Path('pyproject.toml')
        if not path.exists():
            return dict()
        return read_config(path)

    def parse_configuration_and_cli(self, argv: List[str] = None) -> None:
        config, _ = self.option_manager.parse_args([])
        config.__dict__.update(DEFAULTS)
        config.__dict__.update(self.get_toml_config())
        self.options, self.args = aggregate_options(
            manager=self.option_manager,
            config_finder=self.config_finder,
            arglist=argv,
            values=config,
        )
        super().parse_configuration_and_cli(argv=argv)

    def make_file_checker_manager(self):
        self.file_checker_manager = FlakeHellCheckersManager(
            baseline=getattr(self.options, 'baseline', None),
            style_guide=self.guide,
            arguments=self.args,
            checker_plugins=self.check_plugins,
        )

    def find_plugins(self):
        """Patched finder to directly register custom formatters.
        """
        super().find_plugins()
        for name, cls in FORMATTERS.items():
            entry_point = EntryPoint.from_string(
                epstr='{package}.formatters:{class_name}'.format(
                    package=NAME,
                    class_name=cls.__name__,
                ),
                name=name,
            )
            self.formatting_plugins.plugins[name] = Plugin(
                name=name,
                entry_point=entry_point,
                local=True,
            )
            self.formatting_plugins.names.append(name)

    def make_guide(self):
        """Patched StyleGuide creation just to use FlakeHellStyleGuideManager
        instead of original one.
        """
        if self.guide is None:
            self.guide = FlakeHellStyleGuideManager(self.options, self.formatter)

        if self.running_against_diff:
            self.guide.add_diff_ranges(self.parsed_diff)
