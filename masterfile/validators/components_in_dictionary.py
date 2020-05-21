#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

import logging

from masterfile import errors

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate(mf):
    logger.debug('validators.components_in_dictionary:validate()')
    if mf.dictionary is None:
        logger.warning("dictionary is None, can't check")
        return []
    errs = _mf_components_not_in_dictionary(mf)
    logger.debug('found {} errors'.format(len(errs)))
    return errs


def _mf_components_not_in_dictionary(mf):
    errs = []
    for f, df in zip(mf._candidate_data_files, mf._dataframes):
        for i, col in enumerate(df.columns):
            # Note: This returns an empty list for the index, so we don't
            # need to check for it explicitly
            for component, value in mf.column_components(col):
                logger.debug('looking for {} {}'.format(component, value))
                if (component, value) not in mf.dictionary:
                    errs.append(errors.ComponentNotInDictionaryError(
                        message='{} {} not found in dictionary'.format(
                            component, value),
                        locations=[errors.Location.smart_create(
                            filename=f,
                            column_index=i)]
                    ))
    return errs
