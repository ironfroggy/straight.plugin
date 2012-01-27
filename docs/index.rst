.. straight.plugin documentation master file, created by
   sphinx-quickstart on Wed Jan 25 22:49:22 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to straight.plugin's documentation!
===========================================

Contents:

.. toctree::
   :maxdepth: 2

   Loaders <loaders>
   Writing Plugins <write-plugin>


Overview
========

`straight.plugin` is very easy.

Loading all the classes inside a namespace which are subclasses of some
base is the preferred invocation of ``straight.plugin`` loading, and is
straight forward.

::

    from straight.plugin import load

    plugins = load('myplugins', subclasses=FileHandler)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

