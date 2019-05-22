#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from os import path

import pytest

from masterfile.scripts import create


class TestMakeBlankDictionary(object):
    def test_prints_output_on_success_stdout(self, good_path, capsys):
        create.main([good_path, '-'])
        out, err = capsys.readouterr()
        assert len(out) > 0

    def test_prints_output_on_success_outfile(self, good_path, tmpdir):
        outfile = str(tmpdir.join('dict.csv'))
        create.main([good_path, outfile])
        assert path.exists(str(outfile))
        assert path.getsize(str(outfile)) > 0
