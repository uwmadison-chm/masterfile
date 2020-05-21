#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys
from os import path

SETUP_REQUIRES = ['setuptools >= 30.3.0']
SETUP_REQUIRES += ['wheel'] if 'bdist_wheel' in sys.argv else []


def get_locals(filename):
    local_vars = {}
    exec(open(filename, 'r').read(), {}, local_vars)
    return local_vars


metadata = get_locals(path.join('masterfile', '_metadata.py'))

setup(
    name="masterfile",
    setup_requires=SETUP_REQUIRES,
    version=metadata['version'],
    packages=find_packages(),
    keywords="science research data library",
)
