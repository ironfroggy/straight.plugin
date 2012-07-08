Getting Started
===============

Install
^^^^^^^

::

    pip install straight.plugin

That was super easy.

Decide on a Namespace
^^^^^^^^^^^^^^^^^^^^^

You'll want to decide on a :term:`namespace` within your package where you'll
keep your own plugins and where other developers can add more plugins for
your package to use.

For example, if you're writing a log filtering library named ``logfilter`` you may
choose ``logfilter.plugins`` as a package to hold your plugins, so you'll create
the empty package as you would any other python package. However, the only
contents of ``logfilter/plugins/__init__.py`` will be a little bit of special
code telling python this is a :term:`namespace package`.

::

    # This file will not be needed in Python 3.3
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


Now, any modules you place in this package are plugin modules able to be loaded
by ``straight.plugin``.

::

    from straight.plugin import load

    plugins = load("logfilter.plugins")

If you'll be using more plugins than writing them, you should
:doc:`read more <loaders>` about the loaders available and how they work.


Write a Plugin
^^^^^^^^^^^^^^

Writing a plugin is even easier than loading them. There are two important
plugin types to learn: Module plugins and class Plugins. Every module in
your :term:`namespace package` is a module plugin. Every class they define
is a class plugin.

When you load module plugins, you get all of them.

When you load class plugins, you filter them by a common base and only get
those class plugins which inherit it.

Module plugins are simple and usually define a few functions with names
expected by whoever is loading and using the plugins.

::

    # This is a module plugin

    def add_extra(data):
        if 'x' in data and 'y' in data:
            data['z'] = x * y

    # This was a fairly useless plugin

Class plugins are only a little longer, but can be a bit more controlled to
work with. They depend on a common class the plugins inherit, and this would
be defined by the project loading and using the plugins.

::

    # This is a class plugin

    class RstContentParser(ContentPlugin):
        """Parses any .rst files in a bundle."""

        extensions = ('.rst',)

        def parse(self, content_file):
            src = content_file.read()
            return self.parse_string(src)

        def parse_string(self, src):
            parts = publish_parts(source=src, writer_name='html')
            return parts['html_body']

You can fit as many class plugins inside a module plugin as you want, and
to load them instead of the modules you simply pass a ``subclasses``
parameter to ``load()``.

::
    
    from straight.plugin import load

    plugins = load("jules.plugins", subclasses=ContentPlugin)

The resulting set of plugins are all the classes found which inherit from
ContentPlugin. You can do whatever you want with these, but there are some
helpful tools to make it easier to work with Class plugins.

You can easily create instances of all the classes, which gives you a set
of Instance plugins.

::

    instances = plugins.produce()

You can even pass initialization parameters to ``produce()`` and they'll
be used when creating instances of all the classes. You can see the
:ref:`API docs <api-plugin-manager>` for the ``PluginManager`` to see the
other ways you can work with groups of plugins.
