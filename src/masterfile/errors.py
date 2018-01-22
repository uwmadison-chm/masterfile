# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.


from __future__ import absolute_import, unicode_literals

from .vendor import attr
from . import formatters


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


class SettingsError(Error):
    code = 'E8'


class JSONError(SettingsError):
    code = 'E801'


class IOError(Error):
    code = 'E9'


class FileReadError(IOError):
    code = 'E901'


@attr.s
class Location(object):
    """
    """
    # There's always a filename...
    filename = attr.ib()

    # Optional. One-based (no one talks about line number 0)
    line_number = attr.ib(default=None)

    # Optional. One-based (to be consistent with line_number)
    column_number = attr.ib(default=None)

    def format(self, col_as_letters=True):
        return '{}:{}{}'.format(
            self._format_filename(),
            self._format_line_number(),
            self._format_column_number(col_as_letters))

    def _format_filename(self):
        return self.filename

    def _format_line_number(self):
        if self.line_number is None:
            return ''
        return ' line {}'.format(self.line_number)

    def _format_column_number(self, col_as_letters):
        if self.column_number is None:
            return ''
        if col_as_letters:
            return ' column {}'.format(
                formatters.column_number_to_column_id(self.column_number))
        return ' column {}'.format(self.column_number)
