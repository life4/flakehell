# built-in
from unittest.mock import patch

# external
import pytest

# project
from flakehell._constants import KNOWN_PLUGINS
from flakehell._logic import _extractors, extract, get_installed
from flakehell._patched import FlakeHellApplication


@pytest.mark.parametrize('plugin_name', KNOWN_PLUGINS)
def test_smoke_extract(plugin_name):
    codes = extract(plugin_name)
    assert codes

    for code, msg in codes.items():
        assert type(code) is str, 'bad code type'
        assert type(msg) is str, 'bad message type'

        # that's not exactly true but all plugins follow this convention
        assert code[0].isalpha(), 'code must start from letter'
        assert code[0].isupper(), 'code must be uppercase'


@patch('sys.argv', ['flakehell'])
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


def test_no_duplicate_links():
    all_urls = sorted(KNOWN_PLUGINS.values())
    unique_urls = sorted(set(all_urls))
    assert all_urls == unique_urls

    for url in all_urls:
        assert url.startswith('https://')
