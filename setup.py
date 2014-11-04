#!/usr/bin/env python

import os.path
from distutils.core import setup

setup(
    name = 'extranet',
    packages = ['extranet'],
    version = '0.1',
    author = 'Benoît Taine',
    author_email = 'ork@olol.eu',
    description = 'A module to interact with Unify\'s school management system.',
    url = 'https://github.com/ork/python-extranet',
    install_requires=['requests>=2.4.0'],
    )
