#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

import logging

from masterfile.dictionary import Dictionary

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate(mf):
    logger.debug('validators.dictionary_format:validate()')
    data_dict = Dictionary.load_for_masterfile(mf)
    if data_dict is None:
        logger.debug("data_dict is None, can't validate")
        return []
    errlist = list(data_dict.error_list)
    logger.debug("found {} errors".format(len(errlist)))
    return errlist
