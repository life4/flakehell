from pathlib import Path
from typing import Dict, Any, List


import toml
from entrypoints import EntryPoint
from flake8.main.application import Application
from flake8.plugins.manager import Plugin
from flake8.options.aggregator import aggregate_options

from ._checkers import FlakeHellCheckersManager
from ._style_guide import FlakeHellStyleGuideManager
from ..formatters import FORMATTERS
from .._constants import NAME


class FlakeHellApplication(Application):
    """
    Reloaded flake8 original entrypoint to provide support for some features:
    + pyproject.toml support
    + replace CheckersManager to support for `plugins` option
    + register custom formatters
    """

    def get_toml_config(self) -> Dict[str, Any]:
        with Path('pyproject.toml').open('r') as stream:
            config = toml.load(stream)['tool']['flakehell']
            config = dict(config)
            config['plugins'] = dict(config['plugins'])
            return config

    def parse_configuration_and_cli(self, argv: List[str] = None) -> None:
        self.options, self.args = aggregate_options(
            manager=self.option_manager,
            config_finder=self.config_finder,
            arglist=argv,
        )
        self.options.__dict__.update(self.get_toml_config())
        super().parse_configuration_and_cli(argv=argv)

    def make_file_checker_manager(self):
        self.file_checker_manager = FlakeHellCheckersManager(
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
