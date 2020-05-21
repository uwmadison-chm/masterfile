#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from masterfile.masterfile import Masterfile
from masterfile import errors
from masterfile.validators import io


class TestIO(object):

    def test_returns_no_errors_with_good_dir(self, good_mf):
        result = io.validate(good_mf)
        assert len(result) == 0

    def test_file_read_error_for_missing_settings(self, nosettings_mf):
        mf = Masterfile.load_path(nosettings_mf)
        result = io.validate(mf)
        assert len(result) == 1
        assert isinstance(result[0], errors.FileReadError)
