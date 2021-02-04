"""Facility to load plugins."""

import os
import sys

from functools import lru_cache
from imp import find_module
from importlib import import_module

from straight.plugin.manager import PluginManager


def unique_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


class Loader(object):
    """Base loader class. Only used as a base-class for other loaders."""

    def __init__(self, *args, **kwargs):
        self._cache = []
        self.loaded = False

    def _fill_cache(self, *args, **kwargs):
        raise NotImplementedError()

    def load(self, *args, **kwargs):
        if not self.loaded:
            self._fill_cache(*args, **kwargs)
            self._post_fill()
            self._order()
            self.loaded = True
        return PluginManager(self._cache)

    def _meta(self, plugin):
        meta = getattr(plugin, "__plugin__", None)
        return meta

    def _post_fill(self):
        for plugin in self._cache:
            meta = self._meta(plugin)
            if not getattr(meta, "load", True):
                self._cache.remove(plugin)
            for implied_namespace in getattr(meta, "imply_plugins", []):
                plugins = self._cache
                self._cache = self.load(implied_namespace)
                self._post_fill()
                combined = []
                combined.extend(plugins)
                combined.extend(self._cache)
                self._cache = combined

    def _order(self):
        self._cache.sort(key=self._plugin_priority, reverse=True)

    def _plugin_priority(self, plugin):
        meta = self._meta(plugin)
        return getattr(meta, "priority", 0.0)


class ModuleLoader(Loader):
    """Performs the work of locating and loading straight plugins.

    This looks for plugins in every location in the import path.
    """

    def __init__(self, recurse=False):
        super(ModuleLoader, self).__init__()
        self.recurse = recurse

    def _isPackage(self, path):
        pkg_init = os.path.join(path, "__init__.py")
        return os.path.exists(pkg_init)

    def _findPluginFilePaths(self, namespace):
        already_seen = set()

        # Look in each location in the path
        for path in set(sys.path):

            # Within this, we want to look for a package for the namespace
            namespace_rel_path = namespace.replace(".", os.path.sep)
            namespace_path = os.path.join(path, namespace_rel_path)
            try:
                for possible in os.listdir(namespace_path):

                    poss_path = os.path.join(namespace_path, possible)

                    if self._isPackage(poss_path):
                        if self.recurse:
                            subns = ".".join((namespace, possible.split(".py")[0]))
                            for path in self._findPluginFilePaths(subns):
                                yield path
                        base = possible
                    else:
                        base, ext = os.path.splitext(possible)
                        if base == "__init__" or ext != ".py":
                            continue

                    if base not in already_seen:
                        already_seen.add(base)
                        yield os.path.join(namespace, possible)
            except (FileNotFoundError, NotADirectoryError):
                pass

    def _findPluginModules(self, namespace):
        for filepath in self._findPluginFilePaths(namespace):
            path_segments = list(filepath.split(os.path.sep))
            path_segments = [p for p in path_segments if p]
            path_segments[-1] = os.path.splitext(path_segments[-1])[0]
            import_path = ".".join(path_segments)

            try:
                module = import_module(import_path)
            except ImportError:
                # raise Exception(import_path)

                module = None

            if module is not None:
                yield module

    def _fill_cache(self, namespace):
        """Load all modules found in a namespace"""

        modules = self._findPluginModules(namespace)

        self._cache = list(modules)


class ObjectLoader(Loader):
    """Loads classes or objects out of modules in a namespace, based on a
    provided criteria.

    The load() method returns all objects exported by the module.
    """

    def __init__(self, recurse=False):
        super().__init__()
        self.module_loader = ModuleLoader(recurse=recurse)

    def _fill_cache(self, namespace):
        modules = self.module_loader.load(namespace)
        objects = []

        for module in modules:
            for attr_name in dir(module):
                if not attr_name.startswith("_"):
                    objects.append(getattr(module, attr_name))

        self._cache = objects
        return objects


class ClassLoader(ObjectLoader):
    """Loads classes out of plugin modules which are subclasses of a single
    given base class.
    """

    def _fill_cache(self, namespace, subclasses=None):
        objects = super(ClassLoader, self)._fill_cache(namespace)
        classes = []
        for cls in objects:
            if isinstance(cls, type):
                if subclasses is None:
                    classes.append(cls)
                elif issubclass(cls, subclasses) and cls is not subclasses:
                    classes.append(cls)

        self._cache = classes
        return classes


@lru_cache(maxsize=None, typed=False)
def unified_load(namespace, subclasses=None, recurse=False):
    """Provides a unified interface to both the module and class loaders,
    finding modules by default or classes if given a ``subclasses`` parameter.
    """

    if subclasses is not None:
        return ClassLoader(recurse=recurse).load(namespace, subclasses=subclasses)
    else:
        return ModuleLoader(recurse=recurse).load(namespace)
