#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from os import path
import glob

from masterfile.scripts import masterfile as mf


class TestValidateMasterfile(object):
    def test_retval_zero_for_good_dir(self, good_path, capsys):
        retval = mf.main(['validate', good_path])
        out, err = capsys.readouterr()
        assert out.startswith('No problems found')
        assert err == ''
        assert retval == 0

    def test_retval_nonzero_for_bad_dir(self, example_path, capsys):
        retval = mf.main(['validate', example_path])
        out, _err = capsys.readouterr()
        assert not retval == 0
        assert len(out) > 0

    def test_retval_nonzero_for_problems_dir(self, problems_path, capsys):
        retval = mf.main(['validate', problems_path])
        out, _err = capsys.readouterr()
        assert not retval == 0
        assert len(out) > 0
        assert 'problems' in out

    def test_retval_nonzero_for_good_with_problem_files(
            self, good_path, problems_path, capsys):
        problem_file = glob.glob(path.join(problems_path, '*csv'))[0]
        retval = mf.main(['validate', good_path, problem_file])
        out, _err = capsys.readouterr()
        assert not retval == 0
        assert len(out) > 0
        assert 'problems' in out
