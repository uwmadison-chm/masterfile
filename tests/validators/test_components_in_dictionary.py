#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

from masterfile.validators import components_in_dictionary

import logging
components_in_dictionary.logger.setLevel(logging.DEBUG)


class TestColumnFormat(object):
    def test_no_problems_with_good_data(self, full_good_mf):
        errs = components_in_dictionary.validate(full_good_mf)
        assert not errs

    def test_problems_data(self, full_problems_mf):
        errs = components_in_dictionary.validate(full_problems_mf)
        assert errs
