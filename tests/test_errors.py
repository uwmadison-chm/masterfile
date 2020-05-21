#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.


import pytest

from masterfile import errors


class TestLocation(object):
    def test_smart_create_with_filename(self):
        loc = errors.Location.smart_create(filename='foo')
        assert loc.filename == 'foo'

    def test_smart_create_with_line_col_numbers(self):
        loc = errors.Location.smart_create(
            filename='foo', line_number=1, column_number=1)
        assert loc.line_number == 1
        assert loc.column_number == 1

    def test_smart_create_with_row_col_indexes(self):
        loc = errors.Location.smart_create(
            filename='foo', row_index=0, column_index=0)
        assert loc.line_number == 2
        assert loc.column_number == 1

    def test_smart_create_faile_with_conflicting_args(self):
        with pytest.raises(AttributeError):
            errors.Location.smart_create(
                'foo', row_index=0, line_number=0)
        with pytest.raises(AttributeError):
            errors.Location.smart_create(
                'foo', column_index=0, column_number=0)

    def test_smart_create_with_comment(self):
        loc = errors.Location.smart_create('foo', comment='bar')
        assert loc.comment == 'bar'
