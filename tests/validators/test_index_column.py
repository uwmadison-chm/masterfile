#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from ..test_masterfile import GOOD_PATH, PROBLEMS_PATH

import masterfile
from masterfile import errors
from masterfile.validators import index_column


class TestIndexColumnValidator(object):

    def test_returns_no_error_for_good_mf(self):
        mf = masterfile.load(GOOD_PATH)
        ers = index_column.validate(mf)
        assert len(ers) == 0

    def test_returns_error_with_bad_col_id(self):
        mf = masterfile.load(PROBLEMS_PATH)
        ers = index_column.validate(mf)
        assert len(ers) == 1
        assert isinstance(ers[0], errors.IndexNotFoundError)
