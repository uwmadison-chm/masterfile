#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Extract masterfile-formatted data from a CSV file.

Takes a CSV file with a mix of data destined for a masterfile and other data,
and extracts and formats the data to masterfile format, writing the result
to stdout.

Extraction is done based on column header format: we'll extract the index
column, as well as any columns with enough underscores to make up all the
parts of settings.json's "components" entry.

If there's a "comments" or "description" row in your data, you can skip it
with the --skip option. Additionally, rows with blank index_column will
always be skipped, since they don't make any sense in the masterfile data.
"""

from __future__ import absolute_import, unicode_literals

import sys
import re
import logging
from contextlib import contextmanager

import pandas as pd

from masterfile.masterfile import LINE_ENDING
from masterfile.masterfile import Masterfile

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(args):
    import os
    os.linesep = "\r\n"
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args)
    df = pd.read_csv(args.csv_file, dtype=str, na_filter=False)
    mf = Masterfile.load_path(args.masterfile_path)
    formatted = format_dataframe_for_masterfile(
        df, mf, args.index_column, args.skip)
    with file_or_stdout(args.out_file) as output:
        formatted.to_csv(output, line_terminator=LINE_ENDING)


@contextmanager
def file_or_stdout(filename):
    if filename == '-':
        logger.info('Writing to stdout')
        yield sys.stdout
    else:
        with open(filename, 'w', newline=LINE_ENDING) as f:
            logger.info('Writing to {}'.format(filename))
            yield f


def format_dataframe_for_masterfile(df, mf, input_index_col, skip_rows):
    """
    Return a copy of df, with:
    * input_index_col renamed to mf.index_col
    * index_col as the first column
    * only the columns that match the format (c1_c2_..._cN) included
    * rows with index_col as blank excluded
    """
    index_col = mf.index_column
    logger.debug('Original columns: {}'.format(df.columns))
    logger.debug('Original has {} rows'.format(len(df)))
    col_rx = col_match_regex(mf, input_index_col)
    logger.debug('Column regex: {}'.format(col_rx))
    col_filtered = df.filter(regex=col_rx)
    row_filtered = _filter_rows(col_filtered, input_index_col, skip_rows)
    logger.debug('Now has {} rows'.format(len(row_filtered)))
    renamed = row_filtered.rename(columns={input_index_col: index_col})
    renamed.set_index(index_col, inplace=True)
    logger.debug('New columns: {}'.format(renamed.columns))
    return renamed


def _filter_rows(df, index_col, skip_rows):
    skipped = df[skip_rows:]
    has_data = ~(
        (skipped[index_col].str.strip() == '') |
        (skipped[index_col].isnull())
    )
    return skipped[has_data]


def col_match_regex(mf, input_index_col):
    index_col = input_index_col or mf.index_column
    return '(^{}$)|(^{}$)'.format(
        re.escape(index_col), component_col_regex(len(mf.components)))


def component_col_regex(component_count):
    """
    Match things like 'foo_bar_baz_corge'
    """
    return '_'.join(([r'[^_\s]+'] * component_count))


if __name__ == '__main__':
    main()
