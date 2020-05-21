# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

"""
This package contains functions for pretty-printing data — for example,
converting column numbers into Excel-like column identifier strings.
"""

from __future__ import absolute_import

import string


def column_number_to_column_id(number):
    """
    Takes a one-based index and converts it to a column identifier string
    such as used in Excel. Examples:
    0 => A
    25 => Z
    26 => AA
    703 => AAB
    Note that this is similar to converting numbers to base-26, but not quite
    the same — this numbering scheme has no concept of 0. We go from
    "Z" to "AA" which is like going from 9 to 11 with no intervening 10.
    Only works for positive integers.
    """
    if not isinstance(number, int) or number <= 0:
        raise AttributeError(
            "column_number_to_column_id requires a non-negative int")
    digits = string.ascii_uppercase
    parts = []
    while number > 0:
        number, mod = divmod(number - 1, len(digits))
        parts.insert(0, digits[mod])
    return ''.join(parts)
