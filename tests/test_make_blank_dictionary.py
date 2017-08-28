#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

import pytest

from .test_masterfile import GOOD_PATH
from masterfile.scripts import make_blank_dictionary


def test_raises_on_empty_params():
    with pytest.raises(SystemExit):
        make_blank_dictionary.main([])


def prints_output_on_success(capsys):
    make_blank_dictionary.main([GOOD_PATH])
    out, err = capsys.readouterr()
    assert len(out) > 0
