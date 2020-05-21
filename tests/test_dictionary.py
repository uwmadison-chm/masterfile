#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from os import path

from masterfile.dictionary import Dictionary


class TestDictionary(object):
    def test_finds_dictionary_files(self, good_mf):
        d = Dictionary(
            good_mf,
            good_mf.components,
            path.join(good_mf.root_path, 'dictionary'))
        d._find_candidate_files()
        assert d._candidate_files

    def test_reads_unprocessed(self, good_mf):
        d = Dictionary(
            good_mf,
            good_mf.components,
            path.join(good_mf.root_path, 'dictionary'))
        d._find_candidate_files()
        d._read_unprocessed_dataframes()
        assert d._unprocessed_dataframes

    def test_processes_dataframes(self, good_mf):
        d = Dictionary(
            good_mf,
            good_mf.components,
            path.join(good_mf.root_path, 'dictionary'))
        d._find_candidate_files()
        d._read_unprocessed_dataframes()
        d._process_dataframes()
        assert not d.error_list
        assert d._loaded_dataframes
        assert d._loaded_files

    def test_load_for_masterfile(self, good_mf):
        d = Dictionary.load_for_masterfile(good_mf)
        assert d._loaded_dataframes
        assert d._loaded_files

    def test_dict_dataframe(self, good_dict):
        assert 'contact' in good_dict.df.columns

    def test_dict_getitem(self, good_dict):
        result = good_dict['measure', 'foo']
        assert result['contact'] == 'Jordan'  # measure_contacts.csv

    def test_dict_contains(self, good_dict):
        assert ('measure', 'foo') in good_dict
        assert ('measure', 'missing') not in good_dict

    def test_annotations_for(self, good_dict):
        result = good_dict.annotations_for('measure', 'foo')
        assert result['contact'] == 'Jordan'
        assert not good_dict.annotations_for('timepoint', 't1')
        assert not good_dict.annotations_for('missing', 'things')

    def test_load_records_errors(self, problems_mf):
        d = Dictionary.load_for_masterfile(problems_mf)
        assert d.error_list
