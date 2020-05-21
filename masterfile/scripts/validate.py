#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

"""Validate masterfile data, dictionaries, and exclusion files.

Looks through a masterfile directory and loads all data, dictionary, and
exclusion files. Prints a list of warnings and errors for missing data,
ordered by file. Where appropriate, line and column identifiers are also
printed.

If extra files following the masterfile path are given, this program will
check those files' formats in addition to the ones in the masterfile. This
lets you validate files before incorporating them into your data.
"""

from __future__ import absolute_import, unicode_literals

from masterfile.masterfile import Masterfile
from masterfile import validator

import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

CLEAN = 0
ERRORS = 1


def main(args):
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args)
    mf = Masterfile.find_settings_file_and_construct(
        args.masterfile_path)
    mf._find_candidate_data_files()
    mf._candidate_data_files.extend(args.file)
    mf._read_unprocessed_data_files()
    mf._process_dataframes()
    mf._load_dictionary()
    errors = validator.run_all_validators(mf)
    for e in errors:
        print(e.message)
        for loc in e.locations:
            print('  {}'.format(loc.format(True)))
    if errors:
        return ERRORS
    else:
        print("No problems found!")
    return CLEAN


if __name__ == '__main__':
    sys.exit(main())
