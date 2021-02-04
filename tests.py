#!/usr/bin/env python

import os
import sys
import unittest
from types import ModuleType
from unittest import mock

from straight.plugin import loaders, manager

try:
    skipIf = unittest.skipIf
except AttributeError:
    import functools

    class SkipTest(Exception):
        """
        Raise this exception in a test to skip it.

        Usually you can use TestResult.skip() or one of the skipping decorators
        instead of raising this directly.
        """

    def skipIf(cond, reason):
        """
        Unconditionally skip a test.
        """

        def decorator(test_item):
            if cond:
                if not isinstance(test_item, type):

                    @functools.wraps(test_item)
                    def skip_wrapper(*args, **kwargs):
                        pass

                    test_item = skip_wrapper

                test_item.__unittest_skip__ = True
                test_item.__unittest_skip_why__ = reason
                return test_item
            else:
                return test_item

        return decorator


class LoaderTestCaseMixin(object):

    paths = []

    def setUp(self):
        for path in self.paths:
            if isinstance(path, tuple):
                path = os.path.join(*path)
            sys.path.append(path)

        super(LoaderTestCaseMixin, self).setUp()

    def tearDown(self):
        for path in self.paths:
            del sys.path[-1]
        for modname in list(sys.modules):
            if modname.startswith("testplugin"):
                del sys.modules[modname]


class ModuleLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), "test-packages", "more-test-plugins"),
        os.path.join(os.path.dirname(__file__), "test-packages", "some-test-plugins"),
    )

    def setUp(self):
        self.loader = loaders.ModuleLoader()
        super(ModuleLoaderTestCase, self).setUp()

    def test_load(self):
        modules = list(self.loader.load("testplugin"))
        assert len(modules) == 2, modules

    def test_plugin(self):
        assert self.loader.load("testplugin")[0].do(1) == 2


class ImpliedNamespaceModuleTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), "test-packages", "pep-420-plugins"),
    )

    def setUp(self):
        self.loader = loaders.ModuleLoader()
        super(ImpliedNamespaceModuleTestCase, self).setUp()

    @skipIf(sys.version_info < (3, 3), "Python < 3.3")
    def test_load(self):
        modules = list(self.loader.load("testplugin"))
        assert len(modules) == 1, modules

    @skipIf(sys.version_info < (3, 3), "Python < 3.3")
    def test_plugin(self):
        r = self.loader.load("testplugin")[0].do("implied namespace packages are")
        self.assertEqual(r, "implied namespace packages are from pep-420")


class ImplyLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (os.path.join(os.path.dirname(__file__), "test-packages", "imply-plugins"),)

    def setUp(self):
        self.loader = loaders.ModuleLoader()
        super(ImplyLoaderTestCase, self).setUp()

    def test_load(self):
        modules = list(self.loader.load("testplugin"))
        assert len(modules) == 1, modules
        assert modules[0].__name__ == "testplugin_2.bar", modules[0].__name__


class ObjectLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), "test-packages", "more-test-plugins"),
        os.path.join(os.path.dirname(__file__), "test-packages", "some-test-plugins"),
    )

    def setUp(self):
        self.loader = loaders.ObjectLoader()
        super(ObjectLoaderTestCase, self).setUp()

    def test_load_all(self):
        objects = list(self.loader.load("testplugin"))
        self.assertEqual(len(objects), 2, str(objects)[:100] + " ...")


class ClassLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), "test-packages", "class-test-plugins"),
    )

    def setUp(self):
        self.loader = loaders.ClassLoader()
        super(ClassLoaderTestCase, self).setUp()

    def test_all_classes(self):
        classes = list(self.loader.load("testplugin"))

        self.assertEqual(len(classes), 3)

    def test_subclasses(self):
        from testplugin import testclasses

        classes = list(self.loader.load("testplugin", subclasses=testclasses.A))

        self.assertEqual(len(classes), 1)
        self.assertTrue(classes[0] is testclasses.A1)


class PriorityLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), "test-packages", "class-test-plugins"),
    )

    def setUp(self):
        self.loader = loaders.ClassLoader()
        super(PriorityLoaderTestCase, self).setUp()

    def test_all_classes(self):
        classes = list(self.loader.load("testplugin"))

        self.assertEqual(classes[0].__name__, "B")
        self.assertEqual(classes[1].__name__, "A")
        self.assertEqual(classes[2].__name__, "A1")


class PackageLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):
    paths = (
        os.path.join(
            os.path.dirname(__file__), "test-packages", "package-test-plugins"
        ),
    )

    def setUp(self):
        self.loader = loaders.ModuleLoader()
        super(PackageLoaderTestCase, self).setUp()

    def test_find_packages(self):
        filepaths = list(self.loader._findPluginFilePaths("testplugin"))

        self.assertEqual(len(filepaths), 3)

    def test_load_packages(self):
        packages = list(self.loader.load("testplugin"))

        self.assertEqual(len(packages), 3)

        for pkg in packages:
            self.assertTrue(isinstance(pkg, ModuleType))

    def test_plugin(self):
        plugins = self.loader.load("testplugin")

        results = set(p.do(1) for p in plugins)

        self.assertEqual(results, set((2, 3, 4)))


class RecursingPackageLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):
    paths = (
        os.path.join(
            os.path.dirname(__file__), "test-packages", "package-test-plugins"
        ),
    )

    def setUp(self):
        self.loader = loaders.ModuleLoader(recurse=True)
        super(RecursingPackageLoaderTestCase, self).setUp()

    def test_find_packages(self):
        filepaths = list(self.loader._findPluginFilePaths("testplugin"))

        self.assertEqual(len(filepaths), 4)

    def test_load_packages(self):
        packages = list(self.loader.load("testplugin"))

        self.assertEqual(len(packages), 4)

        for pkg in packages:
            self.assertTrue(isinstance(pkg, ModuleType))

    def test_plugin(self):
        plugins = self.loader.load("testplugin")

        results = set(p.do(1) for p in plugins)

        self.assertEqual(results, set((2, 3, 4, "quu")))


class PluginManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.m = manager.PluginManager([mock.Mock(), mock.Mock()])

    def test_first(self):
        self.m._plugins[0].x.return_value = 1

        self.assertEqual(1, self.m.first("x", "a"))
        self.assertFalse(self.m._plugins[1].called)
        self.assertTrue(self.m._plugins[0].called_with("a"))

    def test_pipe(self):
        def plus_one(x):
            return x + 1

        self.m._plugins[0].x.side_effect = plus_one
        self.m._plugins[1].x.side_effect = plus_one
        self.assertEqual(3, self.m.pipe('x', 1))

    def test_pipe_no_plugins_found(self):
        no_plugins = manager.PluginManager([])
        self.assertEqual(1, no_plugins.pipe('x', 1))

    def test_call(self):
        results = self.m.call("x", 1)
        self.assertTrue(self.m._plugins[0].called_with("a"))
        self.assertTrue(self.m._plugins[1].x.called_with(1))

    def test_produce(self):
        products = self.m.produce(1, 2)
        assert products[0] is self.m._plugins[0].return_value
        self.m._plugins[0].called_with(1, 2)
        assert products[1] is self.m._plugins[1].return_value
        self.m._plugins[1].called_with(1, 2)


if __name__ == "__main__":
    unittest.main()
