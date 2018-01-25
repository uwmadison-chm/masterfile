#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

import pytest
from os import path

from masterfile.scripts import validate_masterfile


class TestValidateMasterfile(object):

    def test_raises_on_empty_params(self):
        with pytest.raises(SystemExit):
            validate_masterfile.main([])

    def test_shows_help(self, capsys):
        with pytest.raises(SystemExit):
            validate_masterfile.main(['-h'])
        out, err = capsys.readouterr()
        assert out.startswith('Validate')
        assert err == ''

    def test_retval_zero_for_good_dir(self, good_path, capsys):
        retval = validate_masterfile.main([good_path])
        out, _err = capsys.readouterr()
        assert out == ''
        assert retval == 0

    def test_retval_nonzero_for_bad_dir(self, example_path, capsys):
        retval = validate_masterfile.main([example_path])
        out, _err = capsys.readouterr()
        assert not retval == 0
        assert len(out) > 0

    def test_retval_nonzero_for_problems_dir(self, problems_path, capsys):
        retval = validate_masterfile.main([problems_path])
        out, _err = capsys.readouterr()
        assert not retval == 0
        assert len(out) > 0
