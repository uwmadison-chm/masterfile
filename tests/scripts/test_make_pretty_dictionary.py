#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from os import path

from masterfile.scripts import pretty


class TestMakePrettyDictionary(object):
    def test_writes_output_on_success_file(self, good_path, tmpdir):
        outfile = tmpdir.join('joined.csv')
        pretty.write_pretty_dictionary(good_path, outfile)
        assert path.exists(str(outfile))
        assert path.getsize(str(outfile)) > 0
