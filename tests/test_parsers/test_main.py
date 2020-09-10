# project
from flakehell._constants import DEFAULTS
from flakehell.parsers import PARSERS


def test_default_filename():
    assert {name[1:] for name in DEFAULTS['filename']} == set(PARSERS)
