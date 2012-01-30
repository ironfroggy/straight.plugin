Writing Plugins
===============

Plugins can exist inside your
existing packages or in special namespace packages, which exist
only to house plugins.

The only requirement is that any package containing plugins be
designated a "namespace package", which is currently performed
in Python via the ``pkgutil.extend_path`` utility, seen below.
This allows the namespace to be provided in multiple places on
the python ``sys.path``, where ``import`` looks, and all the
contents will be combined.

Use a :term:`namespace package`

This allows multiple packages installed on your system to share
this name, so they may come from different installed projects
and all combine to provide a larger set of plugins.


Example
-------

::

    # logfilter/__init__.py

    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


::

    # logfilter/hide_extra.py
    
    from logfilter import Skip

    def filter(log_entry):
        level = log_entry.split(':', 1)[0]
        if level != 'EXTRA':
            return log_entry
        else:
            raise Skip()


Using the plugin
''''''''''''''''

In our log tool, we might load all the modules in the ``logfilter``
namespace, and then use them all to process each entry in our logs.
We don't need to know all the filters ahead of time, and other packages
can be installed on a user's system providing additional modules
in the namespace, which we never even knew about.

::

    from straight.plugin import load

    class Skip(Exception):
        pass

    plugins = load('logfilter')

    def filter_entry(log_entry):
        for plugin in plugins:
            try:
                log_entry = plugin.filter(log_entry)
            except Skip:
                pass
        return log_entry
