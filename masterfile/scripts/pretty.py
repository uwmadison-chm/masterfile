#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

""" Re-format the masterfile dictionary to contain every masterfile column

Usage: make_pretty_dictionary [options] <masterfile_path> <outfile>

This is useful for feeding into Excel and browsing or searching around.

Use '-' as outfile to write to stdout.

Options:
  -v, --verbose         Display debugging output
"""

from __future__ import absolute_import, unicode_literals

import sys
from itertools import chain

import pandas

import masterfile
from masterfile.masterfile import LINE_ENDING

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def column_to_tuples(colname, components):
    column_parts = colname.split('_')
    return [
        (colname, '_'.join(dict_key)) for dict_key in zip(
            components, column_parts)
    ]


def columns_to_tuples(columns, components):
    return list(chain(*[column_to_tuples(c, components) for c in columns]))


def columns_to_index(columns, components):
    return pandas.MultiIndex.from_tuples(
        columns_to_tuples(columns, components))


def populate_pretty_df(df, mf):
    d = mf.dictionary
    for index_val, dict_entries in d.df.iterrows():
        logger.debug('Working on {}'.format(index_val))
        key = '_'.join(index_val)
        for dict_col, value in dict_entries.iteritems():
            try:
                df.loc[pandas.IndexSlice[:, key], dict_col] = value
            except KeyError:
                logger.warn(
                    'Dictionary contains unused entry {}'.format(index_val))


def allocate_pretty_df(mf):
    ix = columns_to_index(mf.df.columns, mf.components)
    cols = mf.dictionary.columns
    return pandas.DataFrame(index=ix, columns=cols, dtype=object)


def write_pretty_dictionary(mf_path, output):
    mf = masterfile.load(mf_path)
    pretty_df = allocate_pretty_df(mf)
    pretty_df = pretty_df[~pretty_df.index.duplicated(keep='first')]
    original_index = pretty_df.index
    pretty_df.sort_index(inplace=True)
    populate_pretty_df(pretty_df, mf)
    reindexed = pretty_df.reindex(index=original_index)
    reindexed.to_csv(output, line_terminator=LINE_ENDING)
    return 0


def main(args):
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args)
    output = args.out_file
    if output == '-':
        output = sys.stdout
    return write_pretty_dictionary(args.masterfile_path, output)


if __name__ == '__main__':
    sys.exit(main())
