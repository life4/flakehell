from typing import List

from ._app import FlakeHellApplication


def main(argv: List[str] = None):
    app = FlakeHellApplication(program='flakehell', version='1.0.0')
    app.run(argv)
    app.exit()
