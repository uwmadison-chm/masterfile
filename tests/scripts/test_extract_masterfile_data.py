#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

import pytest
import pandas as pd
from os import path

from masterfile.scripts import extract
from masterfile.scripts import masterfile as mf
from masterfile.masterfile import LINE_ENDING


@pytest.fixture
def df(input_file):
    return pd.read_csv(input_file, dtype=str, na_filter=False)


@pytest.fixture
def input_file(example_path):
    return path.join(example_path, 'foo_input.csv')


class TestExtractMasterfileData(object):
    def test_skip_rows_excludes_blanks(self, df):
        df2 = extract._filter_rows(df, 'id_number', 0)
        assert len(df2) == (len(df) - 1)

    def test_skip_rows_skips(self, df):
        df2 = extract._filter_rows(df, 'id_number', 1)
        assert len(df2) == (len(df) - 2)

    def test_sets_index_column(self, df, good_mf):
        df2 = extract.format_dataframe_for_masterfile(
            df, good_mf, 'id_number', 1)
        assert df2.index.name == good_mf.index_column

    def test_filters_rows(self, df, good_mf):
        df2 = extract.format_dataframe_for_masterfile(
            df, good_mf, 'id_number', 1)
        assert len(df2) == (len(df) - 2)

    def test_filters_columns(self, df, good_mf):
        df2 = extract.format_dataframe_for_masterfile(
            df, good_mf, 'id_number', 1)
        assert len(df2.columns) == (len(df.columns) - 3)

    def test_roundtrip_file(self, input_file, good_path, tmpdir):
        outfile = str(tmpdir.join('output.csv'))
        mf.main([
            'extract',
            '--index_column=id_number',
            '--skip=1',
            good_path,
            input_file,
            outfile])
        out = open(outfile, newline=LINE_ENDING).read()
        lines = out.split(LINE_ENDING)
        assert len(lines) == 11
        assert lines[-1].strip() == ''
        columns = lines[0].split(',')
        assert columns[0] == 'ppt_id'

    def test_roundtrip_stdout(self, input_file, good_path, capsys):
        mf.main([
            'extract',
            '--index_column=id_number',
            '--skip=1',
            good_path,
            input_file,
            '-'])
        out, _err = capsys.readouterr()
        lines = out.split('\r\n')
        assert len(lines) == 11
        assert lines[-1] == ''
        columns = lines[0].split(',')
        assert columns[0] == 'ppt_id'
