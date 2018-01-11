# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.


from __future__ import absolute_import, unicode_literals

from .vendor import attr


@attr.s
class Error(object):

    location = attr.ib()

    message = attr.ib()

    root_exception = attr.ib(default=None)

    code = None


class ColumnError(Error):
    code = 'E1'


class IndexNotFoundError(ColumnError):
    code = 'E101'


class DuplicateColumnError(ColumnError):
    code = 'E102'


class IOError(Error):
    code = 'E9'


class FileReadError(IOError):
    code = 'E901'
