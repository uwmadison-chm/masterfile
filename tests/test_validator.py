#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from masterfile import validator
from masterfile import errors


def instance_filter(iterable, klass):
    return [i for i in iterable if isinstance(i, klass)]


class TestValidator(object):

    def test_good_path_has_no_errors(self, good_mf):
        ers = validator.run_all_validators(good_mf)
        assert len(ers) == 0

    def test_example_path_has_ioerror(self, nosettings_mf):
        ers = validator.run_all_validators(nosettings_mf)
        assert instance_filter(ers, errors.IOError)

    def test_problems_path_has_index_error(self, problems_mf):
        ers = validator.run_all_validators(problems_mf)
        assert instance_filter(ers, errors.IndexNotFoundError)

    def test_probelms_path_has_duplicate_index_error(self, problems_mf):
        assert instance_filter(
            validator.run_all_validators(problems_mf),
            errors.DuplicateIndexValueError)

    def test_probelms_path_has_missing_index_value_error(self, problems_mf):
        assert instance_filter(
            validator.run_all_validators(problems_mf),
            errors.MissingIndexValueError)

    def test_problems_path_has_duplicate_error(self, problems_mf):
        ers = validator.run_all_validators(problems_mf)
        assert instance_filter(ers, errors.DuplicateColumnError)

    def test_problems_path_has_column_format_error(self, problems_mf):
        ers = validator.run_all_validators(problems_mf)
        assert instance_filter(ers, errors.ColumnFormatError)

    def test_problems_path_has_component_not_in_dictionary_error(
            self, full_problems_mf):
        ers = validator.run_all_validators(full_problems_mf)
        assert instance_filter(ers, errors.ComponentNotInDictionaryError)

    def test_problems_path_has_dictionary_index_error(
            self, full_problems_mf):
        ers = validator.run_all_validators(full_problems_mf)
        assert instance_filter(ers, errors.DictionaryIndexNotFoundError)
