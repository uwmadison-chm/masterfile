#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Extract masterfile-formatted data from a CSV file.

Usage: extract_masterfile_data [options] <masterfile_path> <data_file>

Takes a CSV file with a mix of data destined for a masterfile and other data,
and extracts and formats the data to masterfile format, writing the result
to stdout.

Extraction is done based on column header format: we'll extract the index
column, as well as any columns with enough underscores to make up all the
parts of settings.json's "components" entry.

If there's a "comments" or "description" row in your data, you can skip it
with the --skip option. Additionally, rows with blank index_column will
always be skipped, since they don't make any sense in the masterfile data.

Options:
  --index_column=<col>  Use <col> as the input's index column
  --skip=<rows>         Skip <rows> data columns [default: 0]
  -v, --verbose         Display debugging output
"""

from __future__ import absolute_import, unicode_literals

import sys
import re
import logging

import pandas as pd

import masterfile
from masterfile.masterfile import Masterfile
from masterfile.vendor.docopt import docopt

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(argv=None):
    pargs = docopt(__doc__, argv, version=masterfile.__package_version__)
    if pargs['--verbose']:
        logger.setLevel(logging.DEBUG)
    logger.debug(pargs)
    df = pd.read_csv(pargs['<data_file>'], dtype=str)
    mf = Masterfile.load_path(pargs['<masterfile_path>'])
    formatted = format_dataframe_for_masterfile(
        df, mf, pargs['--index_column'], int(pargs['--skip']))
    formatted.to_csv(sys.stdout, line_terminator='\r\n', index=False)


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
    renamed = col_filtered.rename(columns={input_index_col: index_col})
    ordered = _with_index_col_first(renamed, index_col)
    logger.debug('New columns: {}'.format(ordered.columns))
    row_filtered = _filter_rows(ordered, index_col, skip_rows)
    logger.debug('Now has {} rows'.format(len(row_filtered)))
    return row_filtered


def _with_index_col_first(df, index_col):
    clist = list(df.columns)
    logger.debug('Moving {} to first column'.format(index_col))
    logger.debug(clist)
    clist.remove(index_col)
    clist.insert(0, index_col)
    return df.reindex_axis(clist, axis=1)


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
    return '_'.join((['[^_]+'] * component_count))


if __name__ == '__main__':
    main()
