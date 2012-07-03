.. straight.plugin documentation master file, created by
   sphinx-quickstart on Wed Jan 25 22:49:22 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to straight.plugin's documentation!
===========================================

Contents:

.. toctree::
   :maxdepth: 2

   API <api>
   Loaders <loaders>
   Writing Plugins <write-plugin>
   Glossary <glossary>


Overview
========

`straight.plugin` is very easy.

Loading all the classes inside a namespace which are subclasses of some
base is the preferred invocation of ``straight.plugin`` loading, and is
straight forward.

::

    from straight.plugin import load

    plugins = load('myplugins', subclasses=FileHandler)

    handlers = plugins.produce()
    for line in open(filename):
        print handlers.pipe(line)

Plugins are found from a :term:`namespace`, which means the above example
will look for plugins in modules you could access by importing ``myplugins.this``
or ``myplugins.that``, where the modules exist under the ``myplugins``
package. The distinction between a normal package and a namespace package
is very important here, because a namespace package can add modules and
other packages into an existing package, but exists in a separate location
on disk.

The advantage of this is how easily you can create a Python application or
library which others can easily extend. By documenting the plugins your
project loads internally, you can allow others to distribution their own
namespace packages injecting new plugin modules where your code will look
for them, adding new functionality and behavior without any change on your
part, and allowing users to customize their setup by what plugins they
install in their envrionment. You can even split up your project, and
release some components as optional additions to your core package.
    

Learn more:

* Full Documentation: http://readthedocs.org/docs/straightplugin/

* Mailing List: https://groups.google.com/forum/#!forum/straight.plugin

Getting Started
===============

After installing ``straight.plugin`` with ``pip install straight.plugin``,
you'll want to decide on a :term:`namespace` within your package where you'll
keep your own plugins and where other developers can add more plugins for
your package to use.

For example, if you're writing a log filtering library named ``logfilter`` you may
choose ``logfilter.plugins`` as a package to hold your plugins, so you'll create
the empty package as you would any other python package. However, the only
contents of ``logfilter/plugins/__init__.py`` will be a little bit of special
code telling python this is a :term:`namespace package`.

::

    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


Now, any modules you place in this package are plugin modules able to be loaded
by ``straight.plugin``.

::

    from straight.plugin import load

    plugins = load("logfilter.plugins")


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

