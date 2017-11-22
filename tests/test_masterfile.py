#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
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


def test_load_csv_no_error():
    mf = masterfile.Masterfile(index_column='ppt_id', components=[])
    df = mf._load_data_csv(GOOD_CSVS[0])
    assert df.index.name == 'ppt_id'


def test_load_csv_raises_error_when_missing_index_col():
    mf = masterfile.Masterfile(index_column='missing', components=[])
    with pytest.raises(LookupError):
        mf._load_data_csv(GOOD_CSVS[0])


def test_load_multi_works():
    mf = masterfile.Masterfile(index_column='ppt_id', components=[])
    dataframes, errors = mf._load_data_files(GOOD_CSVS)
    assert len(dataframes) == len(GOOD_CSVS)
    assert len(errors) == 0


def test_load_multi_generates_errors():
    mf = masterfile.Masterfile(index_column='missing', components=[])
    dataframes, errors = mf._load_data_files(GOOD_CSVS)
    assert len(dataframes) == 0
    assert len(errors) == len(GOOD_CSVS)


def test_loading_settings_file_works():
    json_data = masterfile.Masterfile._read_settings_json(GOOD_PATH)
    assert json_data['index_column'] == 'ppt_id'
    assert len(json_data['components']) == 4


def test_loading_fails_for_bad_path():
    with pytest.raises(IOError):
        masterfile.Masterfile._read_settings_json(EXAMPLE_PATH)


def test_loading_from_path():
    mf = masterfile.Masterfile.load_path(GOOD_PATH)
    assert mf.index_column == 'ppt_id'
    assert len(mf._dataframes) == len(GOOD_CSVS)


def test_loaded_dataframe_has_proper_index_name():
    mf = masterfile.Masterfile.load_path(GOOD_PATH)
    assert mf.df.index.name == mf.index_column
