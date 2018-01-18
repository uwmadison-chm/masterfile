#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.


import pytest
from os import path
from glob import glob

from masterfile import masterfile

EXAMPLE_PATH = path.join(path.dirname(path.abspath(__file__)), 'examples')
GOOD_PATH = path.join(EXAMPLE_PATH, 'good')
GOOD_CSVS = glob(path.join(GOOD_PATH, '*csv'))
PROBLEMS_PATH = path.join(EXAMPLE_PATH, 'problems')


class TestMasterfile(object):

    def test_masterfile_loads_unprocessed_files(self):
        mf = masterfile.Masterfile(index_column='ppt_id', components=[])
        mf._candidate_data_files = GOOD_CSVS
        mf._read_unprocessed_data_files()
        assert not mf.errors
        assert len(mf._unprocessed_dataframes) == len(GOOD_CSVS)

    def test_read_unprocessed_errors_on_missing_files(self):
        mf = masterfile.Masterfile(index_column='ppt_id', components=[])
        mf._candidate_data_files = ['bogus.csv']
        mf._read_unprocessed_data_files()
        assert len(mf.errors) == 1

    def test_process_dataframes_sets_index(self):
        mf = masterfile.Masterfile(index_column='ppt_id', components=[])
        mf._candidate_data_files = GOOD_CSVS
        mf._read_unprocessed_data_files()
        mf._process_dataframes()
        assert not mf.errors
        assert len(mf._dataframes) == len(GOOD_CSVS)
        for df in mf._dataframes:
            assert df.index.name == mf.index_column

    def test_process_dataframes_errors_on_missing_column(self):
        mf = masterfile.Masterfile(index_column='missing', components=[])
        mf._candidate_data_files = GOOD_CSVS
        mf._read_unprocessed_data_files()
        mf._process_dataframes()
        assert len(mf.errors) == len(GOOD_CSVS)
        assert len(mf._dataframes) == 0
        assert len(mf._unprocessed_dataframes) == len(GOOD_CSVS)

    def test_loading_settings_file_works(self):
        mf = masterfile.Masterfile.load_path(GOOD_PATH)
        assert mf.index_column == 'ppt_id'
        assert len(mf.components) == 4

    def test_loading_fails_for_bad_path(self):
        mf = masterfile.Masterfile.load_path(EXAMPLE_PATH)
        assert len(mf.errors) == 1

    def test_loading_from_path(self):
        mf = masterfile.Masterfile.load_path(GOOD_PATH)
        assert mf.index_column == 'ppt_id'
        assert len(mf._dataframes) == len(GOOD_CSVS)

    def test_loaded_dataframe_has_proper_index_name(self):
        mf = masterfile.Masterfile.load_path(GOOD_PATH)
        assert mf.df.index.name == mf.index_column
