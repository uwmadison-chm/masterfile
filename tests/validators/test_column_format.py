#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from masterfile import errors
from masterfile.validators import column_format


class TestColumnFormat(object):
    def test_no_errors_on_good_data(self, good_mf):
        ers = column_format.validate(good_mf)
        assert not ers

    def test_errors_on_problem_data(self, problems_mf):
        ers = column_format.validate(problems_mf)
        assert ers
        assert isinstance(ers[0], errors.ColumnFormatError)
        # I'm not sure if I should include this test, it's so data-specific...
        assert len(ers) == 3
