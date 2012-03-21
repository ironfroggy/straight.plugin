Full Documentation: http://readthedocs.org/docs/straightplugin/
Mailing List: https://groups.google.com/forum/#!forum/straight.plugin

# straight.plugin

straight.plugin is a Python plugin loader inspired by twisted.plugin with two
important distinctions:

 - Fewer dependencies
 - Python 3 compatible

The system is used to allow multiple Python packages to provide plugins within
a namespace package, where other packages will locate and utilize. The plugins
themselves are modules in a namespace package where the namespace identifies
the plugins in it for some particular purpose or intent.

For example, if I was building a log parser, I might tell users that he parser
will look for plugins in the `logfilter` namespace. Someone else could then
provide a module named `logfilter.normalizedates` and my parser would find this
plugin, load it, and use it to filter the log entries.

It would be up to me to document what the plugin actually looks like, based on
how I need to use it in my project.

## Using plugins

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

## Writing plugins

    # logfilter/__init__.py
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

    
    # logfilter/hide_extra.py

    from logfilter import Skip

    def filter(log_entry):
        level = log_entry.split(':', 1)[0]
        if level != 'EXTRA':
            return log_entry
        else:
            raise Skip()

## Module and Class Plugins

straight.plugin is able to load both modules and classes, depending on your
needs. When you call `load()` with a namespace, you'll get all the modules
found under that namespace. When you call it with the optional `subclasses`
parameter, all the classes which are subclases of the given type will be
given.

    # Example

    from straight.plugins import load

    plugins = load("ircclient", subclasses=IrcClientCommand)


