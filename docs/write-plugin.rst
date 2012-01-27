Writing Plugins
===============

Writing plugins is an easy process. Plugins can exist inside your
existing packages or in special namespace packages, which exist
only to house plugins.

The only requirement is that any package containing plugins be
designated a "namespace package", which is currently performed
in Python via the ``pkgutil.extend_path`` utility, seen below.

This allows multiple packages installed on your system to share
this name, so they may come from different installed projects
and all combine to provide a larger set of plugins.

Example
-------

logfilter/__init__.py
'''''''''''''''''''''

::

    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


logfilter/hide_extra.py
'''''''''''''''''''''''

::
    
    from logfilter import Skip

    def filter(log_entry):
        level = log_entry.split(':', 1)[0]
        if level != 'EXTRA':
            return log_entry
        else:
            raise Skip()
