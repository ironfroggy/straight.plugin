"""Facility to load plugins."""

import sys
import os


class StraightPluginLoader(object):
    """Performs the work of locating and loading straight plugins.
    
    This looks for plugins in every location in the import path.
    """

    def _findPluginModules(self, namespace):
        already_seen = set()

        # Look in each location in the path
        for path in sys.path:

            # Within this, we want to look for a package for the namespace
            namespace_rel_path = namespace.replace(".", os.path.sep)
            namespace_path = os.path.join(path, namespace_rel_path)
            if os.path.exists(namespace_path):
                for possible in os.listdir(namespace_path):
                    if possible == '__init__.py':
                        continue
                    if possible not in already_seen:
                        already_seen.add(possible)
                        yield os.path.join(namespace_path, possible)
