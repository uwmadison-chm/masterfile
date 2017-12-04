#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Make a blank template dictionary.

Usage: make_blank_dictionary [options] <masterfile_path> <outfile>

Takes a set of masterfile-formatted data files and outputs a dictionary with
one row per component * label to <outfile>. Use '-' for <outfile> to write to
stdout.

Options:
  -v, --verbose  Display debugging output
"""

from __future__ import absolute_import, unicode_literals

import sys
import logging
from collections import defaultdict
from contextlib import contextmanager

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
    with file_or_stdout(pargs['<outfile>']) as output:
        print_blank_dictionary(pargs['<masterfile_path>'], output)


@contextmanager
def file_or_stdout(filename):
    if filename == '-':
        yield sys.stdout
    else:
        with open(filename, 'w') as f:
            yield f


def print_blank_dictionary(pathname, output):
    mf = Masterfile.load_path(pathname)
    mapping = column_components(mf)
    for component in mf.components:
        for val in mapping[component]:
            output.write('{},{}\r\n'.format(component, val))


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
