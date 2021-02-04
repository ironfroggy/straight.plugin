class PluginManager(object):
    def __init__(self, plugins):
        self._plugins = plugins

    def __iter__(self):
        return iter(self._plugins)

    def __len__(self):
        return len(self._plugins)

    def __getitem__(self, index):
        return self._plugins[index]

    def produce(self, *args, **kwargs):
        """Produce a new set of plugins, treating the current set as plugin
        factories.
        """

        new_plugins = []
        for p in self._plugins:
            r = p(*args, **kwargs)
            new_plugins.append(r)
        return PluginManager(new_plugins)

    def call(self, methodname, *args, **kwargs):
        """Call a common method on all the plugins, if it exists."""

        for plugin in self._plugins:
            method = getattr(plugin, methodname, None)
            if method is None:
                continue
            yield method(*args, **kwargs)

    def first(self, methodname, *args, **kwargs):
        """Call a common method on all the plugins, if it exists. Return the
        first result (the first non-None)
        """

        for r in self.call(methodname, *args, **kwargs):
            if r is not None:
                return r

        raise ValueError("No plugins returned a non-None value")

    def pipe(self, methodname, first_arg, *args, **kwargs):
        """Call a common method on all the plugins, if it exists. The return
        value of each call becomes the replaces the first argument in the given
        argument list to pass to the next.

        Useful to utilize plugins as sets of filters.
        """
        r = first_arg
        for plugin in self._plugins:
            method = getattr(plugin, methodname, None)
            if method is None:
                continue
            r = method(first_arg, *args, **kwargs)
            if r is not None:
                first_arg = r
        return r
