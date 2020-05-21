#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from masterfile.validators import duplicate_column


class TestDuplicateColumn(object):
    def test_no_errors_on_good_data(self, good_mf):
        ers = duplicate_column.validate(good_mf)
        assert not ers

    def test_errors_on_problem_data(self, problems_mf):
        ers = duplicate_column.validate(problems_mf)
        assert ers

    def test_map_column_locations_finds_index_dupe_others_not(self, good_mf):
        cmap = duplicate_column._map_column_locations(good_mf)
        assert (
            len(cmap[good_mf.index_column]) ==
            len(good_mf._candidate_data_files)
        )
        del cmap[good_mf.index_column]
        for col, locations in cmap.items():
            assert len(locations) == 1

    def test_find_duplicate_columns_empty_for_good_data(self, good_mf):
        cmap = duplicate_column._find_duplicate_columns(good_mf)
        assert not cmap.keys()

    def test_find_duplicate_columns_finds_duplicates(self, problems_mf):
        cmap = duplicate_column._find_duplicate_columns(problems_mf)
        assert len(cmap.keys()) == 2
        foo_dup_filenames = [loc.filename for loc in cmap['dup_t1_one_file']]
        assert len(set(foo_dup_filenames)) == 1
        bar_dup_filenames = [loc.filename for loc in cmap['dup_t1_two_files']]
        assert len(set(bar_dup_filenames)) == 2
