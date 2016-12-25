# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description = """
This is a generic library that provides support for dictionary-based
permissions with logic gates such as AND and OR. You can register any
kind of permission types such as roles and flags. The idea with this
library is to be an ultra-flexible foundation that can be used by any
framework. It supports python 2 and 3.

INSTALLATION

pip install logical-permissions

USAGE

Please refer to https://github.com/Ordermind/logical-permissions-py for documentation.
"""

setup(
  name = 'logical-permissions',
  version = '1.2.2',
  license = 'MIT',
  description = 'Provides support for dictionary-based permissions with logic gates such as AND and OR.',
  long_description = long_description,
  url = 'https://github.com/Ordermind/logical-permissions-py',
  author = 'Kristofer Tengström',
  author_email = 'ordermind@gmail.com',
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
  keywords = 'permissions',
  packages = find_packages(exclude=['tests*']),
)
