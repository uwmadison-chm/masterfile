#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from masterfile.formatters import index_to_column_id

import pytest


class TestFormatters(object):

    def test_index_to_column_id_normal_inputs(self):
        assert index_to_column_id(0) == 'A'
        assert index_to_column_id(25) == 'Z'
        assert index_to_column_id(26) == 'AA'
        assert index_to_column_id(27) == 'AB'

    def test_index_to_column_id_bad_inputs(self):
        with pytest.raises(AttributeError):
            index_to_column_id('A')
        with pytest.raises(AttributeError):
            index_to_column_id(1.1)
        with pytest.raises(AttributeError):
            index_to_column_id(-1)
