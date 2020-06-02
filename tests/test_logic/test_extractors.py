# external
import pytest

# project
from flakehell._constants import KNOWN_PLUGINS
from flakehell._logic import extract, get_installed, _extractors
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


@pytest.mark.parametrize('plugin_name', KNOWN_PLUGINS)
def test_no_custom_extractor_needed(plugin_name):
    extractor = getattr(_extractors, 'extract_' + plugin_name, None)
    if extractor is None:
        return
    custom_codes = extractor()
    default_codes = _extractors.extract_default(plugin_name)
    assert default_codes != custom_codes
