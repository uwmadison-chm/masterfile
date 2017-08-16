#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_masterfile
----------------------------------

Tests for `masterfile` module.
"""

import pytest
from os import path
from glob import glob

from masterfile import masterfile

EXAMPLE_PATH = path.join(path.dirname(path.abspath(__file__)), 'examples')
GOOD_PATH = path.join(EXAMPLE_PATH, 'good')
GOOD_CSVS = glob(path.join(GOOD_PATH, '*csv'))


def test_load_csv_no_error():
    mf = masterfile.Masterfile(index_column='ppt_id', components=[])
    df = mf._load_csv(GOOD_CSVS[0])
    assert df.index.name == 'ppt_id'


def test_load_csv_raises_error_when_missing_index_col():
    mf = masterfile.Masterfile(index_column='missing', components=[])
    with pytest.raises(LookupError):
        mf._load_csv(GOOD_CSVS[0])


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
