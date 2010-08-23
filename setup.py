#!/usr/bin/env python
from setuptools import setup
from openstates import __version__

long_description = open('README.rst').read()

setup(name="python-openstates",
      version=__version__,
      py_modules=['openstates'],
      description="Library for interacting with the Open State Project API",
      author="Michael Stephens",
      author_email="mstephens@sunlightfoundation.com",
      license="BSD",
      url="http://github.com/sunlightlabs/python-openstates",
      long_description=long_description,
      platforms=["any"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      install_requires=["remoteobjects >= 1.1"]
      )
