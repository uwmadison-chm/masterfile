#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

import logging

from itertools import chain

from masterfile import errors

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate(mf):
    logger.debug("validators.column_format:validate()")
    if mf.components is None:
        logger.debug("no components for this masterfile")
        return []
    ers = _misformatted_column_errors(mf)
    logger.debug("validators.column_format found {} errors".format(len(ers)))
    return ers


def _misformatted_column_errors(mf):
    return [
        errors.ColumnFormatError(
            message="column {} has {} components".format(
                col['column'], col['count']),
            locations=[errors.Location.smart_create(
                filename=col['filename'], column_index=col['index'])]
        )
        for col in _masterfile_misformatted_columns(mf)
    ]


def _masterfile_misformatted_columns(mf):
    icol = mf.index_column
    component_count = len(mf.components)
    mf_errors = [
        _dataframe_misformatted_files(df, fname, component_count, icol)
        for df, fname in
        zip(mf._unprocessed_dataframes, mf._candidate_data_files)
    ]

    return chain(*mf_errors)


def _dataframe_misformatted_files(
        df, filename, masterfile_component_count, index_column):
    misformatted_columns = []
    for i, col in enumerate(df.columns):
        if col == index_column:
            continue
        ccount = len(col.split('_'))
        if not ccount == masterfile_component_count:
            misformatted_columns.append({
                'index': i,
                'column': col,
                'count': ccount,
                'filename': filename
            })
    return misformatted_columns
