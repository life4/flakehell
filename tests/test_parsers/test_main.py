from flakehell.parsers import PARSERS
from flakehell._constants import DEFAULTS


def test_default_filename():
    assert {name[1:] for name in DEFAULTS['filename']} == set(PARSERS)
