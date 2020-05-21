# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.


from __future__ import absolute_import, unicode_literals

import attr
from . import formatters


@attr.s
class Error(object):

    locations = attr.ib()

    message = attr.ib()

    root_exception = attr.ib(default=None)

    code = None

    @property
    def sorted_locations(self):
        def location_key(loc):
            if not hasattr(loc, 'filename'):
                return [loc, None, None]
            return [loc.filename, loc.line_number, loc.column_number]
        return sorted(self.locations, key=location_key)


class ColumnError(Error):
    code = 'E1'


class DuplicateColumnError(ColumnError):
    code = 'E101'


class ColumnFormatError(ColumnError):
    code = 'E102'


class ComponentNotInDictionaryError(ColumnError):
    code = 'E103'


class IndexError(Error):
    code = 'E2'


class IndexNotFoundError(IndexError):
    code = 'E201'


class DuplicateIndexValueError(IndexError):
    code = 'E202'


class MissingIndexValueError(IndexError):
    code = 'E203'


class DictionaryError(Error):
    code = 'E3'


class DictionaryIndexNotFoundError(DictionaryError):
    code = 'E301'


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

    comment = attr.ib(default=None)

    @classmethod
    def smart_create(
            klass,
            filename,
            line_number=None,
            column_number=None,
            row_index=None,
            column_index=None,
            comment=None):
        if (line_number is not None and row_index is not None):
            raise AttributeError(
                "Can't specify both line_number and row_index")

        if (column_number is not None and column_index is not None):
            raise AttributeError(
                "Can't specify both column_number and column_index")

        if row_index is not None:
            # One for the header row, one for one-based indexing
            line_number = row_index + 2

        if column_index is not None:
            column_number = column_index + 1

        return klass(
            filename=filename,
            line_number=line_number,
            column_number=column_number,
            comment=comment)

    def format(self, col_as_letters=True):
        return '{}{}{}{}'.format(
            self._format_filename(),
            self._format_line_number(),
            self._format_column_number(col_as_letters),
            self._format_comment())

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

    def _format_comment(self):
        if self.comment is None:
            return ''
        return ' ({})'.format(self.comment)
