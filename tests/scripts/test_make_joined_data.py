#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

import pytest

from os import path

from masterfile.scripts import make_joined_data


class TestMakeJoinedData(object):

    def test_raises_on_empty_params(self):
        with pytest.raises(SystemExit):
            make_joined_data.main([])

    def test_prints_output_on_success_file(self, good_path, tmpdir):
        outfile = tmpdir.join('joined.csv')
        make_joined_data.make_joined_data(good_path, outfile)
        assert path.exists(str(outfile))
        assert path.getsize(str(outfile)) > 0

    def test_prints_output_on_success_stdout(self, good_path, capsys):
        make_joined_data.main([good_path, '-'])
        out, _err = capsys.readouterr()
        assert len(out) > 0
