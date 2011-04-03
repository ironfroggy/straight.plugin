#!/usr/bin/env python

import unittest

from straight.plugin.loader import StraightPluginLoader


class PluginTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = StraightPluginLoader()

    def test_load(self):
        modules = list(self.loader.load('testplugin'))
        assert len(modules) == 1, modules

    def test_plugin(self):
        assert self.loader.load('testplugin')[0].do(1) == 2


if __name__ == '__main__':
    unittest.main()
