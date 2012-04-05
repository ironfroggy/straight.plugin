Glossary
-------------

.. glossary::
    :sorted:

    package
        A Python package is a module defined by a directory, containing
        a ``__init__.py`` file, and can contain other modules or other
        packages within it.

        ::
        
            package/
                __init__.py
                subpackage/
                    __init__.py
                submodule.py

        see also, :term:`namespace package`

    distribution
        Separately installable sets of Python modules as stored in the
        Python package index, and installed by distutils or setuptools.

        *definition taken from* `PEP 382`_ *text*

    vendor package
        Groups of files installed by an operating system's packaging
        mechanism (e.g. Debian or Redhat packages install on Linux systems).
        
        *definition taken from* `PEP 382`_ *text*

    namespace package
        Mechanism for splitting a single Python package across multiple
        directories on disk. One or more distributions (see :term:`distribution`)
        may provide modules which exist inside the same :term:`namespace package`.

        *definition taken from* `PEP 382`_ *text*

    module
        An importable python namespace defined in a single file.


.. _PEP 382: http://www.python.org/dev/peps/pep-0382/
