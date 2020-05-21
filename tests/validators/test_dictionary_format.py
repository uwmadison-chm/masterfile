#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from masterfile.validators import dictionary_format


class TestDictionaryFormat(object):
    def test_good_masterfile_has_no_errors(self, good_mf):
        errors = dictionary_format.validate(good_mf)
        assert not errors

    def test_problems_dict_has_errors(self, problems_mf):
        errors = dictionary_format.validate(problems_mf)
        assert len(errors) > 0
