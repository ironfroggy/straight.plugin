#!/usr/bin/env python

from distutils.core import setup

setup(name='straight.plugin',
      version='1.2',
      description='A simple namespaced plugin facility',
      author='Calvin Spealman',
      author_email='ironfroggy@gmail.com',
      url='https://github.com/ironfroggy/straight.plugin',
      packages=['straight', 'straight.plugin'],
     )
