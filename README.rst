Full Documentation: http://readthedocs.org/docs/straightplugin/
Mailing List: https://groups.google.com/forum/#!forum/straight.plugin

Straight Plugin is very easy.

Straight Plugin provides a type of plugin you can create
from almost any existing Python modules, and an easy way for outside developers
to add functionality and customization to your projects with their own
plugins.

Using any available plugins is a snap.

::

    from straight.plugin import load

    plugins = load('theproject.plugins', subclasses=FileHandler)

    handlers = plugins.produce()
    for line in open(filename):
        print handlers.pipe(line)


And, writing plugins is just as easy.

::

    from theproject import FileHandler

    class LineNumbers(FileHandler):
        def __init__(self):
            self.lineno = 0
        def pipe(line):
            self.lineno += 1
            return "%04d %s" % (self.lineno, line)

Plugins are found from a :term:`namespace`, which means the above example
would find any ``FileHandler`` classes defined in modules you might import
as ``theproject.plugins.default`` or ``theproject.plugins.extra``. Through
the magic of :term:`namespace packages <namespace package>`, we can even
split these up into separate installations, even managed by different teams.
This means you can ship a project with a set of default plugins implementing
its behavior, and allow other projects to hook in new functionality simply
by shipping their own plugins under the same :term:`namespace`.

:doc:`Get started and learn more, today <getting-started>`
