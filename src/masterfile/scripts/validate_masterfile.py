#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

"""Validate masterfile data, dictionaries, and exclusion files.

Usage: validate_masterfile [options] <masterfile_path>

Looks through a masterfile directory and loads all data, dictionary, and
exclusion files. Prints a list of warnings and errors for missing data,
ordered by file. Where appropriate, line and column identifiers are also
printed.

Options:
  -v, --verbose         Display debugging output
"""

from __future__ import absolute_import, unicode_literals

import masterfile
from masterfile import validator
from masterfile.vendor.docopt import docopt

import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

CLEAN = 0
ERRORS = 1


def main(argv=None):
    pargs = docopt(__doc__, argv, version=masterfile.__package_version__)
    if pargs['--verbose']:
        logger.setLevel(logging.DEBUG)
    logger.debug(pargs)
    mf = masterfile.masterfile.Masterfile.load_path(pargs['<masterfile_path>'])
    errors = validator.run_all_validators(mf)
    for e in errors:
        print(e.message)
        for loc in e.locations:
            print('  {}'.format(loc.format(True)))
    if errors:
        return ERRORS
    return CLEAN


if __name__ == '__main__':
    sys.exit(main())
