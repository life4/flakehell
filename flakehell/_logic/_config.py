from pathlib import Path
from typing import Any, Dict

import urllib3
import toml


def read_config(*paths) -> Dict[str, Any]:
    config = dict()
    for path in paths:
        if isinstance(path, Path):
            new_config = _read_local(path)
        elif Path(path).exists():
            new_config = _read_local(Path(path))
        else:
            new_config = _read_remote(path)
        config = _merge_configs(config, new_config)
    return config


def _read_local(path: Path):
    with path.open('r') as stream:
        return _parse_config(stream.read())


def _read_remote(url: str):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return _parse_config(response.data.decode())


def _merge_configs(*configs):
    config = dict()
    for subconfig in configs:
        config.update(subconfig)

    config['plugins'] = dict()
    for subconfig in configs:
        config['plugins'].update(subconfig.get('plugins', {}))

    return config


def _parse_config(content: str):
    config = toml.loads(content).get('tool', {}).get('flakehell', {})
    config = dict(config)
    if 'plugins' in config:
        config['plugins'] = dict(config['plugins'])

    if 'base' in config:
        paths = config['base']
        if not isinstance(paths, list):
            paths = [paths]
        config = _merge_configs(read_config(*paths), config)

    return config
