from pathlib import Path
from typing import Dict, Any, List


import toml
from flake8.main.application import Application
from flake8.options.aggregator import aggregate_options
from ._checkers import FlakeHellCheckersManager


class FlakeHellApplication(Application):

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
