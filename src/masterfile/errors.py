# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.


from __future__ import absolute_import, unicode_literals

from .vendor import attr


@attr.s
class Error(object):

    code = attr.ib()

    location = attr.ib()

    message = attr.ib()


ERROR_CODES = {
    'E1': 'Columns',
    'E101': 'index column not found',
    'E102': 'duplicate column name'
}
