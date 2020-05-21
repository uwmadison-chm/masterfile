#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.


from masterfile import masterfile


class TestMasterfile(object):

    def test_masterfile_loads_unprocessed_files(self, good_csvs):
        mf = masterfile.Masterfile(index_column='ppt_id', components=[])
        mf._candidate_data_files = good_csvs
        mf._read_unprocessed_data_files()
        assert not mf.errors
        assert len(mf._unprocessed_dataframes) == len(good_csvs)

    def test_read_unprocessed_errors_on_missing_files(self):
        mf = masterfile.Masterfile(index_column='ppt_id', components=[])
        mf._candidate_data_files = ['bogus.csv']
        mf._read_unprocessed_data_files()
        assert len(mf.errors) == 1

    def test_process_dataframes_sets_index(self, good_csvs):
        mf = masterfile.Masterfile(index_column='ppt_id', components=[])
        mf._candidate_data_files = good_csvs
        mf._read_unprocessed_data_files()
        mf._process_dataframes()
        assert not mf.errors
        assert len(mf._dataframes) == len(good_csvs)
        for df in mf._dataframes:
            assert df.index.name == mf.index_column

    def test_process_dataframes_errors_on_missing_column(self, good_csvs):
        mf = masterfile.Masterfile(index_column='missing', components=[])
        mf._candidate_data_files = good_csvs
        mf._read_unprocessed_data_files()
        mf._process_dataframes()
        assert len(mf.errors) == len(good_csvs)
        assert len(mf._dataframes) == 0
        assert len(mf._unprocessed_dataframes) == len(good_csvs)

    def test_loading_settings_file_works(self, good_path):
        mf = masterfile.Masterfile.load_path(good_path)
        assert mf.index_column == 'ppt_id'
        assert len(mf.components) == 4

    def test_loading_fails_for_bad_path(self, example_path):
        mf = masterfile.Masterfile.load_path(example_path)
        assert len(mf.errors) == 1

    def test_loading_from_path(self, good_path, good_csvs):
        mf = masterfile.Masterfile.load_path(good_path)
        assert mf.index_column == 'ppt_id'
        assert len(mf._dataframes) == len(good_csvs)

    def test_loaded_dataframe_has_proper_index_name(self, good_path):
        mf = masterfile.Masterfile.load_path(good_path)
        assert mf.df.index.name == mf.index_column

    def test_load_and_annotate(self, good_path):
        mf = masterfile.Masterfile.load_and_annotate(good_path)
        assert mf.dictionary is not None
        assert mf.df.sr_t1_foo_var1.contact['measure_foo'] == 'Jordan'

    def test_module_level_load(self, good_path):
        mf = masterfile.load(good_path)
        assert mf.dictionary is not None
        assert mf.df.sr_t1_foo_var1.contact['measure_foo'] == 'Jordan'
