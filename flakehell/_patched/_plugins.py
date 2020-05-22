# built-in
from collections import defaultdict

# external
from flake8.plugins.manager import Checkers, PluginManager


class MultiDict:
    def __init__(self):
        self._data = defaultdict(list)

    def get(self, name: str, default=None):
        items = self._data[name]
        if items:
            return items[0]
        return default

    def getlist(self, name: str, default=None) -> list:
        items = self._data[name]
        if items:
            return items
        return default

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        self._data[name].append(value)

    def items(self):
        for name, values in self._data.items():
            for value in values:
                yield name, value

    def values(self):
        for values in self._data.values():
            for value in values:
                yield value


class FlakeHellPluginManager(PluginManager):
    def __init__(self, namespace, local_plugins=None):
        self.namespace = namespace
        self.plugins = MultiDict()
        self.names = []
        self._load_local_plugins(local_plugins or [])
        self._load_entrypoint_plugins()

    def map(self, func, *args, **kwargs):
        for plugin in self.plugins.values():
            yield func(plugin, *args, **kwargs)

    def versions(self):
        plugins_seen = set()
        for plugin in self.plugins.values():
            plugin_name = plugin.plugin_name
            if plugin.plugin_name in plugins_seen:
                continue
            plugins_seen.add(plugin_name)
            yield (plugin_name, plugin.version)


class FlakeHellCheckers(Checkers):
    def __init__(self, local_plugins=None):
        self.manager = FlakeHellPluginManager(
            namespace=self.namespace,
            local_plugins=local_plugins,
        )
        self.plugins_loaded = False
