# built-in
import json
from hashlib import md5
from pathlib import Path
from time import time
from typing import Optional

# external
from flake8.checker import FileChecker
from flake8.options.manager import OptionManager


CACHE_PATH = Path.home() / '.cache' / 'flakehell'
THRESHOLD = 3600 * 24  # 1 day


def prepare_cache(path=CACHE_PATH):
    if not path.exists():
        path.mkdir(parents=True)
        return
    for fpath in path.iterdir():
        if time() - fpath.stat().st_atime <= THRESHOLD:
            continue
        fpath.unlink()


class Snapshot:
    _exists: Optional[bool] = None
    _digest: Optional[str] = None
    _results = None

    def __init__(self, *, cache_path: Path, file_path: Path):
        self.cache_path = cache_path
        self.file_path = file_path

    @classmethod
    def create(cls, checker: FileChecker, options: OptionManager) -> 'Snapshot':
        hasher = md5()

        # plugins config
        plugins = json.dumps(options.plugins, sort_keys=True)
        hasher.update(plugins.encode())

        # file path
        file_path = Path(checker.filename).resolve()
        hasher.update(str(file_path).encode())

        return cls(
            cache_path=CACHE_PATH / (hasher.hexdigest() + '.json'),
            file_path=file_path,
        )

    def exists(self) -> bool:
        """Returns True if cache file exists and is actual.
        """
        if self._exists is not None:
            return self._exists

        if not self.cache_path.exists():
            self._exists = False
            return self._exists

        # digest is None for non-existent files (stdin)
        if self.digest is None:
            return False

        # check that file content wasn't changed since the snapshot
        cache = json.loads(self.cache_path.read_text())
        self._exists = self.digest == cache['digest']
        # if cache is valid results will be eventually requested.
        # let's save it for later use to avoid reading the cache twice
        if self._exists:
            self._results = cache['results']
        return self._exists  # type: ignore

    @property
    def digest(self) -> Optional[str]:
        """Get hex digest for the current content of the file
        """
        # we cache it because it requested twice: from `exists` and from `dumps`
        if self._digest is None:
            if not self.file_path.exists():
                return None
            hasher = md5()
            hasher.update(self.file_path.read_bytes())
            self._digest = hasher.hexdigest()
        return self._digest

    def dump(self, results) -> None:
        self.cache_path.write_text(self.dumps(results=results))

    def dumps(self, results) -> str:
        return json.dumps(dict(
            results=results,
            digest=self.digest,
        ))

    @property
    def results(self):
        """returns cached checks results for the given file
        """
        # results could be cached from `.exists()`.
        # however, we don't want to cache the results on requets
        # because they are always requested only once
        if self._results is not None:
            return self._results
        return json.loads(self.cache_path.read_text())['results']
