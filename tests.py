#!/usr/bin/env python

import sys
import os
import unittest

from straight.plugin import loaders


class ModuleLoaderTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = loaders.ModuleLoader()
        sys.path.append(os.path.join(os.path.dirname(__file__), 'test-packages', 'more-test-plugins'))
        sys.path.append(os.path.join(os.path.dirname(__file__), 'test-packages', 'some-test-plugins'))

    def tearDown(self):
        del sys.path[-1]
        del sys.path[-1]

    def test_load(self):
        modules = list(self.loader.load('testplugin'))
        assert len(modules) == 2, modules

    def test_plugin(self):
        assert self.loader.load('testplugin')[0].do(1) == 2


class SelectiveLoaderTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = loaders.ObjectLoader()
        sys.path.append(os.path.join(os.path.dirname(__file__), 'test-packages', 'more-test-plugins'))
        sys.path.append(os.path.join(os.path.dirname(__file__), 'test-packages', 'some-test-plugins'))

    def tearDown(self):
        del sys.path[-1]
        del sys.path[-1]

    def test_load_all(self):
        objects = list(self.loader.load('testplugin'))
        self.assertEqual(len(objects), 2, str(objects)[:100] + ' ...')


if __name__ == '__main__':
    unittest.main()
