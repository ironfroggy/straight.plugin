Plugin Loaders
==============

Currently, three simple loaders are providerd.


ClassLoader
-----------

The recommended loader is the ``ClassLoader``, used to load all the
classes from all of the modules in the namespace given. Optionally,
you can pass a ``subclasses`` parameter to ``load()``, which will
filter the loaded classes to those which are a sub-class of any given
type.

For example,

::

    import os
    from straight.plugin.loaders import ClassLoader
    from myapp import FileHandler

    plugins = ClassLoader().load('myplugins', subclasses=FileHandler)

    for filename in os.listdir('.'):
        for handler_cls in plugins:
            handler = handler_cls(filename)
            if handler.valid():
                handler.process()

However, it is preferred that you use the ``load()`` helper provided.

::

    from straight.plugin import load

    plugins = load('myplugins', subclasses=FileHandler)

This will automatically use the ``ClassLoader`` when given a ``subclasses``
argument.


ModuleLoader
------------

Before anything else, ``straight.plugin`` loads modules. The
``ModuleLoader`` is used to do this.

::

    from straight.plugin.loaders import ModuleLoader

    plugins = ModuleLoader().load('myplugins')


ObjectLoader
------------

If you need to combine multiple plugins inside each module, you can
load all the objects from the modules, rather than the modules themselves.

::

    from straight.plugin.loaders import ObjectLoader
    
    plugins = ObjectLoader().load('myplugins')


