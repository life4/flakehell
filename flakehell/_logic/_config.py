from pathlib import Path
from typing import Any, Dict

import urllib3
import toml


def read_config(*paths) -> Dict[str, Any]:
    config = dict()
    for path in paths:
        if isinstance(path, Path):
            config.update(_read_local(path))
            continue
        if Path(path).exists():
            config.update(_read_local(Path(path)))
            continue
        config.update(_read_remote(path))
    if 'plugins' not in config:
        config['plugins'] = dict()
    return config


def _read_local(path: Path):
    with path.open('r') as stream:
        return _parse_config(stream.read())


def _read_remote(url: str):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return _parse_config(response.data.decode())


def _parse_config(content: str):
    config = toml.loads(content)['tool']['flakehell']
    config = dict(config)
    if 'plugins' in config:
        config['plugins'] = dict(config['plugins'])

    if 'base' in config:
        paths = config['base']
        if not isinstance(paths, list):
            paths = [paths]
        old_config = config
        config = read_config(*paths)
        config.update(old_config)

    return config
