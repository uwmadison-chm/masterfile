#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Make a blank template dictionary.

Takes a set of masterfile-formatted data files and outputs a dictionary with
one row per component * label to <outfile>. Use '-' for <outfile> to write to
stdout.
"""

from __future__ import absolute_import, unicode_literals

import sys
import logging
from collections import defaultdict
from contextlib import contextmanager

from masterfile.masterfile import Masterfile

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(args):
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args)
    with file_or_stdout(args.out_file) as output:
        print_blank_dictionary(args.masterfile_path, output)


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
