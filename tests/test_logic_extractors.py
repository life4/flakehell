import pytest

from flakehell._logic import extract
from flakehell._constants import KNOWN_PLUGINS


@pytest.mark.parametrize('plugin_name', KNOWN_PLUGINS)
def test_smoke_extract(plugin_name):
    codes = extract(plugin_name)
    assert codes
