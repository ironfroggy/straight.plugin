#!/usr/bin/env python

import sys
from setuptools import setup, find_packages


setup(
    name="straight.plugin",
    version="1.4.2",
    description="A simple namespaced plugin facility",
    author="Calvin Spealman",
    author_email="ironfroggy@gmail.com",
    url="https://github.com/ironfroggy/straight.plugin",
    packages=find_packages(),
    namespace_packages=["straight"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Environment :: Plugins",
    ],
)
