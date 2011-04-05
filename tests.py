#!/usr/bin/env python

import sys
import os
import unittest

from straight.plugin.loader import StraightPluginLoader


class PluginTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = StraightPluginLoader()
        sys.path.append(os.path.join(os.path.dirname(__file__), 'more-test-plugins'))
        sys.path.append(os.path.join(os.path.dirname(__file__), 'some-test-plugins'))

    def tearDown(self):
        del sys.path[-1]
        del sys.path[-1]

    def test_load(self):
        modules = list(self.loader.load('testplugin'))
        assert len(modules) == 2, modules

    def test_plugin(self):
        assert self.loader.load('testplugin')[0].do(1) == 2


if __name__ == '__main__':
    unittest.main()
