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


def item_row_dict(mf, column, component, part):
    dict_df = mf.dictionary.dataframe
    row_dict = {
        'item': column,
        'compoment': component,
        'value': part
    }
    try:
        dict_entry = dict_df.loc[(component, part)]
        row_dict.update(dict_entry)
    except KeyError:
        logger.warn(f"{(component, part)} not found in dictionary")
    return row_dict


def make_pretty_df(mf, condense=True):
    """
    Make a dictionary-equivalent that lists every single column in the
    masterfile, along with any dictionary metadata that goes with it.
    The 'condense' option avoids printing overly-repetitive data.

    In this case, "overly-repetitive" means it won't repeat components if
    only the last component changes -- so, for example, if you have
    sr_panas_pa
    sr_panas_na
    sr_ffmq_observe
    sr_ffmq_actAware

    sr and panas will only be printed for sr_panas_pa and sr_ffmq_observe
    """
    df = mf.dataframe
    cols = df.columns
    last_seen_most_sig = None
    df_data = []
    for col in cols:
        col_parts = col.split("_")
        components = mf.components
        most_sig_parts = col_parts[:-1]
        if last_seen_most_sig == most_sig_parts and condense:
            col_parts = col_parts[-1:]
            components = components[-1:]
        for part, component in zip(col_parts, components):
            df_data.append(item_row_dict(mf, col, component, part))
        last_seen_most_sig = most_sig_parts
    return pandas.DataFrame(df_data)


def write_pretty_dictionary(mf_path, output, condense=True):
    mf = masterfile.load(mf_path)
    pretty = make_pretty_df(mf, condense)
    pretty.to_csv(output, index=False)
    return 0


def main(args):
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args)
    output = args.out_file
    if output == '-':
        output = sys.stdout
    return write_pretty_dictionary(args.masterfile_path, output, args.condense)


if __name__ == '__main__':
    sys.exit(main())
