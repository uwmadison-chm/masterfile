#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Join all masterfile data into a single .csv file

Usage: make_joined_data [options] <masterfile_path> <outfile>

Useful for processing in languages that don't have easy support for joining
a bunch of csv files into one.

Use '-' as outfile to write to stdout.

Options:
  -v, --verbose         Display debugging output
"""

from __future__ import absolute_import, unicode_literals

import sys

import masterfile
from masterfile.vendor.docopt import docopt

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def make_joined_data(masterfile_path, output_file):
    mf = masterfile.load(masterfile_path)
    mf.dataframe.to_csv(output_file, line_terminator='\r\n')


def main(argv=None):
    pargs = docopt(__doc__, argv, version=masterfile.__package_version__)
    if pargs['--verbose']:
        logger.setLevel(logging.DEBUG)
    logger.debug(pargs)
    output = pargs['<outfile>']
    if output == '-':
        logger.info("sgtdout")
        output = sys.stdout
    make_joined_data(pargs['<masterfile_path>'], output)


if __name__ == '__main__':
    main()
