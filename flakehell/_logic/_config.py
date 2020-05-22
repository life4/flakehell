# built-in
from pathlib import Path
from typing import Any, Dict

# external
import toml
import urllib3


def read_config(*paths) -> Dict[str, Any]:
    config = dict()  # type: Dict[str, Any]
    for path in paths:
        if isinstance(path, Path):
            new_config = _read_local(path)
        elif path.startswith(('https://', 'http://')):
            new_config = _read_remote(path)
        elif Path(path).exists():
            new_config = _read_local(Path(path))
        else:
            new_config = _read_remote(path)
        config = _merge_configs(config, new_config)
    return config


def _read_local(path: Path) -> Dict[str, Any]:
    with path.open('r') as stream:
        return _parse_config(stream.read())


def _read_remote(url: str) -> Dict[str, Any]:
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return _parse_config(response.data.decode())


def _merge_configs(*configs) -> Dict[str, Any]:
    config = dict()
    for subconfig in configs:
        config.update(subconfig)

    for section in ('plugins', 'exceptions'):
        config[section] = dict()
        for subconfig in configs:
            config[section].update(subconfig.get(section, {}))

    return config


def _parse_config(content: str) -> Dict[str, Any]:
    config = toml.loads(content).get('tool', {}).get('flakehell', {})
    config = dict(config)

    for section in ('plugins', 'exceptions'):
        if section in config:
            config[section] = dict(config[section])

    if 'base' in config:
        paths = config['base']
        if not isinstance(paths, list):
            paths = [paths]
        config = _merge_configs(read_config(*paths), config)

    return config
