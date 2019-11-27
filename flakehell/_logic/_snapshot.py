import json
from hashlib import md5
from pathlib import Path
from time import time

from flake8.checker import FileChecker
from flake8.options.manager import OptionManager

from ._plugin import get_plugin_name, get_plugin_rules


CACHE_PATH = Path.home() / '.cache' / 'flakehell'
THRESHOLD = 3600  # 1 hour


def prepare_cache(path=CACHE_PATH):
    if not path.exists():
        path.mkdir(parents=True)
        return
    for fpath in path.iterdir():
        if time() - fpath.stat().st_atime <= THRESHOLD:
            continue
        fpath.unlink()


class Snapshot:
    _exists = None

    def __init__(self, digest):
        self.digest = digest
        self.path = CACHE_PATH / (self.digest + '.json')

    @classmethod
    def create(cls, checker: FileChecker, options: OptionManager):
        hasher = md5()
        # plugin info
        for chunk in checker.display_name[:-1]:
            hasher.update(chunk.encode())
        # file path
        path = Path(checker.filename).resolve()
        hasher.update(str(path).encode())
        # file content
        hasher.update(path.read_bytes())

        # plugins config
        plugin_name = get_plugin_name(checker.check)
        rules = get_plugin_rules(
            plugin_name=plugin_name,
            plugins=options.plugins,
        )
        hasher.update('|'.join(rules).encode())

        return cls(digest=hasher.hexdigest())

    def exists(self) -> bool:
        if self._exists is None:
            self._exists = self.path.exists()
        return self._exists

    def dump(self, results) -> None:
        self.path.write_text(self.dumps(results=results))

    def dumps(self, results) -> str:
        return json.dumps(results)

    def get_results(self):
        return json.loads(self.path.read_text())
