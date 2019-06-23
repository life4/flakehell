import sys
from typing import List

from ._app import FlakeHellApplication
from ._discover import discover
from ._extractors import extract


def main(argv: List[str] = None):
    if argv is None:
        argv = sys.argv[1:]
    app = FlakeHellApplication(program='flakehell', version='1.0.0')
    if argv[0] == 'lint':
        app.run(argv[1:])
        app.exit()

    if argv[0] == 'installed':
        plugins = sorted(discover(app=app, argv=argv[1:]), key=lambda p: p['name'])
        width = max(len(p['name']) for p in plugins)
        for plugin in plugins:
            print('{} | {}'.format(plugin['name'].ljust(width), ', '.join(plugin['codes'])))
        sys.exit(0)

    if argv[0] == 'show':
        codes = extract(argv[1])
        width = max(len(code) for code in codes)
        for code, info in sorted(codes.items()):
            print('{} | {}'.format(code.ljust(width), info))
        sys.exit(0)
