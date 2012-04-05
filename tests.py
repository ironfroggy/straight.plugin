#!/usr/bin/env python

import sys
import os
import unittest
from types import ModuleType

from straight.plugin import loaders


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
            if modname.startswith('testplugin'):
                del sys.modules[modname]


class ModuleLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), 'test-packages', 'more-test-plugins'),
        os.path.join(os.path.dirname(__file__), 'test-packages', 'some-test-plugins'),
    )
    
    def setUp(self):
        self.loader = loaders.ModuleLoader()
        super(ModuleLoaderTestCase, self).setUp()
    
    def test_load(self):
        modules = list(self.loader.load('testplugin'))
        assert len(modules) == 2, modules

    def test_plugin(self):
        assert self.loader.load('testplugin')[0].do(1) == 2


class ImplyLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), 'test-packages', 'imply-plugins'),
    )
    
    def setUp(self):
        self.loader = loaders.ModuleLoader()
        super(ImplyLoaderTestCase, self).setUp()
    
    def test_load(self):
        modules = list(self.loader.load('testplugin'))
        assert len(modules) == 1, modules
        assert modules[0].__name__ == 'testplugin_2.bar', modules[0].__name__


class ObjectLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), 'test-packages', 'more-test-plugins'),
        os.path.join(os.path.dirname(__file__), 'test-packages', 'some-test-plugins'),
    )

    def setUp(self):
        self.loader = loaders.ObjectLoader()
        super(ObjectLoaderTestCase, self).setUp()

    def test_load_all(self):
        objects = list(self.loader.load('testplugin'))
        self.assertEqual(len(objects), 2, str(objects)[:100] + ' ...')


class ClassLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), 'test-packages', 'class-test-plugins'),
    )

    def setUp(self):
        self.loader = loaders.ClassLoader()
        super(ClassLoaderTestCase, self).setUp()

    def test_all_classes(self):
        classes = list(self.loader.load('testplugin'))

        self.assertEqual(len(classes), 3)

    def test_subclasses(self):
        from testplugin import testclasses
        classes = list(self.loader.load('testplugin', subclasses=testclasses.A))

        self.assertEqual(len(classes), 1)
        self.assertTrue(classes[0] is testclasses.A1)

class PriorityLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):

    paths = (
        os.path.join(os.path.dirname(__file__), 'test-packages', 'class-test-plugins'),
    )

    def setUp(self):
        self.loader = loaders.ClassLoader()
        super(PriorityLoaderTestCase, self).setUp()

    def test_all_classes(self):
        classes = list(self.loader.load('testplugin'))

        self.assertEqual(classes[0].__name__, 'B')
        self.assertEqual(classes[1].__name__, 'A')
        self.assertEqual(classes[2].__name__, 'A1')

class PackageLoaderTestCase(LoaderTestCaseMixin, unittest.TestCase):
    paths = (
        os.path.join(os.path.dirname(__file__), 'test-packages', 'package-test-plugins'),
    )

    def setUp(self):
        self.loader = loaders.ModuleLoader()
        super(PackageLoaderTestCase, self).setUp()
    
    def test_find_packages(self):
        filepaths = list(self.loader._findPluginFilePaths('testplugin'))

        self.assertEqual(len(filepaths), 2)

    def test_load_packages(self):
        packages = list(self.loader.load('testplugin'))

        self.assertEqual(len(packages), 2)

        for pkg in packages:
            self.assertTrue(isinstance(pkg, ModuleType))
    
    def test_plugin(self):
        plugins = self.loader.load('testplugin')

        results = set(p.do(1) for p in plugins)

        self.assertEqual(results, set((2, 3)))

if __name__ == '__main__':
    unittest.main()
