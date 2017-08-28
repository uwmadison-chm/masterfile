#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Make a blank template dictionary.

Usage: make_blank_dictionary [options] <path>

Takes a set of masterfile-formatted data files and outputs a dictionary with
one row per component * label to stdout.

Options:
  -v, --verbose  Display debugging output
"""

import sys
import logging
from collections import defaultdict

import masterfile
from masterfile.masterfile import Masterfile  # Okay this is ridiculous
from masterfile.vendor.docopt import docopt

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(argv=None):
    pargs = docopt(__doc__, argv, version=masterfile.__package_version__)
    if pargs['--verbose']:
        logger.setLevel(logging.DEBUG)
    logger.debug(pargs)

    print_blank_dictionary(pargs['<path>'])


def print_blank_dictionary(pathname):
    mf = Masterfile.load_path(pathname)
    mapping = column_components(mf)
    for component in mf.components:
        for val in mapping[component]:
            sys.stdout.write('{},{}\r\n'.format(component, val))


def column_components(mf):
    """
    Given a masterfile, break down all of the columns into {component: lables}
    mappings. The return type will be a dict, with strings as the keys and sets
    as the values.
    """
    columns = mf.df.columns
    mapping = defaultdict(set)
    for col in columns:
        parts = col.split('_')
        for index, component in enumerate(mf.components):
            mapping[component].add(parts[index])
    return mapping



if __name__ == '__main__':
    main()
