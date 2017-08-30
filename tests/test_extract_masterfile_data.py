#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

import pytest
import pandas as pd
from os import path

from .test_masterfile import EXAMPLE_PATH, GOOD_PATH
from masterfile.scripts import extract_masterfile_data

INPUT_FILE = path.join(EXAMPLE_PATH, 'foo_input.csv')


@pytest.fixture
def df():
    return pd.read_csv(INPUT_FILE, dtype=str)


def test_raises_on_empty_params():
    with pytest.raises(SystemExit):
        extract_masterfile_data.main([])


def test_skip_rows_excludes_blanks(df):
    df2 = extract_masterfile_data._filter_rows(df, 'id_number', 0)
    assert len(df2) == (len(df) - 1)


def test_skip_rows_skips(df):
    df2 = extract_masterfile_data._filter_rows(df, 'id_number', 1)
    assert len(df2) == (len(df) - 2)


def test_with_index_col_reorders(df):
    df2 = extract_masterfile_data._with_index_col_first(df, 'thing1')
    assert df2.columns[0] == 'thing1'
