#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from os import path

from masterfile import dictionary
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
        assert d._loaded_dataframes
        assert d._loaded_files

    def test_load_processes_dataframes(self, good_mf):
        d = Dictionary.load_for_masterfile(good_mf)
        assert d._loaded_dataframes
        assert d._loaded_files
