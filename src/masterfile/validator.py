# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

"""
The Validator takes a masterfile path and runs a set of checks on the contents.
We validate:

* All data files have the index column as the first column
* There are no blanks in the index column
* There are no repeats in the index column for a file
* All other columns have len(components) parts, separated by _
* No column names are repeated
* All component parts are included in the dictionary
* There are no dictionary entries not represented in the data files
* Places with missing data have exlusion codes

As we do this, we'll keep track of where the data is from, so we can tell
people where the data are from.
"""

from __future__ import absolute_import, unicode_literals

from itertools import chain

from masterfile import validators


VALIDATOR_CHAIN = [
    validators.io,
    validators.index_column,
    validators.duplicate_column,
]


def run_all_validators(masterfile):
    return list(chain(*[m.validate(masterfile) for m in VALIDATOR_CHAIN]))
