#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

import masterfile
from masterfile import validator
from masterfile import errors

from .test_masterfile import EXAMPLE_PATH, GOOD_PATH, PROBLEMS_PATH


def instance_filter(iterable, klass):
    return [i for i in iterable if isinstance(i, klass)]


class TestValidator(object):

    def test_good_path_has_no_errors(self):
        mf = masterfile.load(GOOD_PATH)
        ers = validator.run_all_validators(mf)
        assert len(ers) == 0

    def test_example_path_has_ioerror(self):
        mf = masterfile.load(EXAMPLE_PATH)
        ers = validator.run_all_validators(mf)
        assert instance_filter(ers, errors.IOError)

    def test_problems_path_has_index_error(self):
        mf = masterfile.load(PROBLEMS_PATH)
        ers = validator.run_all_validators(mf)
        assert instance_filter(ers, errors.IndexNotFoundError)
