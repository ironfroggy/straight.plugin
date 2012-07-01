import straight.plugin


class PluginManager(object):

    def __init__(self, loader=None):
        self.loader = loader
        self._plugins = []

    def load(self, *args, **kwargs):
        if self.loader is None:
            new_plugins = straight.plugin.load(*agrs, **kwargs)
        else:
            raise TypeError("PluginManager cannot load without a loader.")
        self._plugins.extend(new_plugins)

    def __iter__(self):
        return iter(self._plugins)

    def __len__(self):
        return len(self._plugins)

    def __getitem__(self, index):
        return self._plugins[index]

    def produce(self, *args, **kwargs):
        new_plugin_set = PluginManager()
        for p in self._plugins:
            r = p(*args, **kwargs)
            new_plugin_set._plugins.append(r)
        return new_plugin_set

    def call(self, method, *args, **kwargs):
        for plugin in self._plugins:
            method = getattr(plugin, method, None)
            if method is None:
                continue
            yield method(*args, **kwargs)

    def first(self, method, *args, **kwargs):
        for r in self.call(method, *args, **kwargs):
            if r is not None:
                return r

        raise ValueError("No plugins returned a non-None value")

    def pipe(self, methodname, first_arg, *args, **kwargs):
        for plugin in self._plugins:
            method = getattr(plugin, methodname, None)
            if method is None:
                continue
            r = method(first_arg, *args, **kwargs)
            if r is not None:
                first_arg = r
        return r

