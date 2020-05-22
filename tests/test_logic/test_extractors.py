# external
import pytest

# project
from flakehell._constants import KNOWN_PLUGINS
from flakehell._logic import extract, get_installed
from flakehell._patched import FlakeHellApplication


@pytest.mark.parametrize('plugin_name', KNOWN_PLUGINS)
def test_smoke_extract(plugin_name):
    codes = extract(plugin_name)
    assert codes


@pytest.mark.parametrize('plugin_name', KNOWN_PLUGINS)
def test_smoke_prefixes(plugin_name):
    app = FlakeHellApplication(program='test', version='1.0.0')
    plugins = {plugin['name']: plugin for plugin in get_installed(app=app)}
    plugin = plugins[plugin_name]

    codes = extract(plugin_name)
    for code in codes:
        print(plugin_name, code, plugin['codes'])
        assert code.startswith(tuple(plugin['codes']))
