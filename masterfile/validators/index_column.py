# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

import logging
from collections import defaultdict

from masterfile import errors

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate(mf):
    logger.debug('validators.index_column:validate()')
    missing_errs = _find_missing_index_columns(mf)
    duplicate_errs = _find_masterfile_duplicate_indexes(mf)
    missing_value_errs = _find_missing_index_values(mf)
    errlist = missing_errs + duplicate_errs + missing_value_errs
    logger.debug("found {} errors".format(len(errlist)))
    return errlist


def _find_missing_index_columns(mf):
    return [e for e in mf.errors if isinstance(e, errors.IndexNotFoundError)]


def _find_masterfile_duplicate_indexes(mf):
    error_list = []
    for f, df in zip(mf._candidate_data_files, mf._unprocessed_dataframes):
        duplicates = _find_dataframe_duplicate_indexes(
            df, mf.index_column, f)
        for val, locations in duplicates.items():
            error_list.append(errors.DuplicateIndexValueError(
                message='duplicate index value {}'.format(val),
                locations=locations
            ))
    return error_list


def _find_dataframe_duplicate_indexes(df, index_column_name, filename):
    if index_column_name not in df:
        return {}
    index_col = df[index_column_name]
    index_locations = defaultdict(list)
    for i, index_val in enumerate(index_col):
        loc = errors.Location.smart_create(
            filename=filename, row_index=i)
        index_locations[index_val].append(loc)
    duplicate_locations = {
        index_val: locations
        for index_val, locations in index_locations.items()
        if len(locations) > 1
    }
    return duplicate_locations


def _find_missing_index_values(mf):
    error_list = []
    for f, df in zip(mf._candidate_data_files, mf._unprocessed_dataframes):
        if mf.index_column not in df:
            continue
        blank_row_indexes = df.index[
            df[mf.index_column].fillna('').str.strip() == '']
        blank_row_locations = [
            errors.Location.smart_create(filename=f, row_index=i)
            for i in blank_row_indexes
        ]
        if not blank_row_locations:
            continue
        error_list.append(errors.MissingIndexValueError(
            message='blank index value',
            locations=blank_row_locations
        ))
    return error_list
