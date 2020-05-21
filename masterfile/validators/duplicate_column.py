#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import

import logging
from collections import defaultdict

from masterfile import errors

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate(mf):
    logger.debug('validators.duplicate_column:validate()')
    duplicates = _find_duplicate_columns(mf)
    errlist = [
        errors.DuplicateColumnError(
            locations=locations,
            message='duplicate column {}'.format(col)
        )
        for col, locations in duplicates.items()
    ]
    logger.debug('found {} errors'.format(len(errlist)))
    return errlist


def _map_column_locations(mf):
    """
    Find all the places where a column is used. Algorithm:

    * Start a column_locations dict. Keys will be column names, values will
      be lists of locations.
    * Iterate over all individual masterfiles
      * Iterate over all columns as column_name
        * For each column, append it location (filename, column number)
          to column_locations[column_name]
    * Return column_locations
    """
    column_locations = defaultdict(list)
    for f, df in zip(mf._candidate_data_files, mf._unprocessed_dataframes):
        for col_index, col_name in enumerate(df.columns):
            column_locations[col_name].append(errors.Location.smart_create(
                filename=f, column_index=col_index))
    return column_locations


def _find_duplicate_columns(mf):
    """
    Find every column that occurs more than once in the masterfile data,
    except for the index column.
    """
    column_locations = _map_column_locations(mf)
    dupes = {
        column_name: locations
        for (column_name, locations) in column_locations.items()
        if (len(locations) > 1 and (not column_name == mf.index_column))
    }
    return dupes
