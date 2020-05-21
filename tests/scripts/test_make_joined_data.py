#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from os import path

from masterfile.scripts import join
from masterfile.scripts import masterfile as mf


class TestMakeJoinedData(object):

    def test_prints_output_on_success_file(self, good_path, tmpdir):
        outfile = tmpdir.join('joined.csv')
        join.make_joined_data(good_path, outfile)
        assert path.exists(str(outfile))
        assert path.getsize(str(outfile)) > 0

    def test_prints_output_on_success_stdout(self, good_path, capsys):
        mf.main(['join', good_path, '-'])
        out, _err = capsys.readouterr()
        assert len(out) > 0
