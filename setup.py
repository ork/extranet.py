#!/usr/bin/env python

import os.path
from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name = "extranet",
    packages = ["extranet"],
    version = "0.1",
    description = "A module to interact with Unify's school management system.",
    author = "Benoît Taine",
    author_email = "benoit.taine@efrei.net",
    url = "https://github.com/ork/extranet.py",
    download_url = "https://github.com/ork/extranet.py/tarball/master",
    license = "GNU LGPL v3",
    keywords = ["school", "api", "client"],
    classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Development Status :: 4 - Beta",
            "Environment :: Other Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
    long_description = README
    )

