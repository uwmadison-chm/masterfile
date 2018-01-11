#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

import pytest

from os import path

from .test_masterfile import GOOD_PATH
from masterfile.scripts import make_joined_data


class TestMakeJoinedData(object):

    def test_raises_on_empty_params(self):
        with pytest.raises(SystemExit):
            make_joined_data.main([])

    def test_prints_output_on_success_file(self, tmpdir):
        outfile = tmpdir.join('joined.csv')
        make_joined_data.make_joined_data(GOOD_PATH, outfile)
        assert path.exists(str(outfile))
        assert path.getsize(str(outfile)) > 0

    def test_prints_output_on_success_stdout(self, capsys):
        make_joined_data.main([GOOD_PATH, '-'])
        out, _err = capsys.readouterr()
        assert len(out) > 0
