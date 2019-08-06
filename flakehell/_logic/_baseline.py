from hashlib import md5


def make_baseline(path: str, context: str, code: str, line: int) -> str:
    digest = md5()
    digest.update(path.encode())
    digest.update((context or str(line)).encode())
    digest.update(code.encode())
    return digest.hexdigest()
