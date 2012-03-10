#!/usr/bin/env python

from distutils.core import setup

setup(name='straight.plugin',
    version='1.3',
    description='A simple namespaced plugin facility',
    author='Calvin Spealman',
    author_email='ironfroggy@gmail.com',
    url='https://github.com/ironfroggy/straight.plugin',
    packages=['straight', 'straight.plugin'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Environment :: Plugins',
    ]
)
