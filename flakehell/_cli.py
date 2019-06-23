import json
import sys
from typing import List

from ._app import FlakeHellApplication
from ._discover import discover


def main(argv: List[str] = None):
    if argv is None:
        argv = sys.argv[1:]
    app = FlakeHellApplication(program='flakehell', version='1.0.0')
    if argv[0] == 'lint':
        app.run(argv[1:])
        app.exit()

    if argv[0] == 'list':
        for plugin in discover(app=app, argv=argv[1:]):
            if plugin['name'] == 'pycodestyle':
                continue
            print('{:30} {}'.format(plugin['name'], ', '.join(plugin['codes'])))
        sys.exit(0)
