#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from masterfile.validators import index_column


class TestIndexColumn(object):

    def test_returns_no_error_for_good_mf(self, good_mf):
        ers = index_column.validate(good_mf)
        assert len(ers) == 0

    def test_returns_error_with_bad_col_id(self, problems_mf):
        ers = index_column._find_missing_index_columns(problems_mf)
        assert ers

    def test_returns_error_with_duplicate_col(self, problems_mf):
        ers = index_column._find_masterfile_duplicate_indexes(problems_mf)
        assert ers

    def test_returns_error_with_missing_value(self, problems_mf):
        ers = index_column._find_missing_index_values(problems_mf)
        assert ers
        locs = ers[0].locations
        assert len(locs) == 2

    def test_returns_error_with_duplicate_index_values(self, problems_mf):
        ers = index_column._find_masterfile_duplicate_indexes(problems_mf)
        assert ers
