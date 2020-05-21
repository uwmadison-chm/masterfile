#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Join all masterfile data into a single .csv file

Useful for processing in languages that don't have easy support for joining
a bunch of csv files into one.
"""

from __future__ import absolute_import, unicode_literals

import sys

import masterfile
from masterfile.masterfile import LINE_ENDING

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def make_joined_data(masterfile_path, output_file):
    mf = masterfile.load(masterfile_path)
    mf.dataframe.to_csv(output_file, line_terminator=LINE_ENDING)


def main(args):
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args)
    output = args.out_file
    if output == '-':
        logger.info("stdout")
        output = sys.stdout
    make_joined_data(args.masterfile_path, output)


if __name__ == '__main__':
    main()
