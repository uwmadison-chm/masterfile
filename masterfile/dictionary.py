# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

"""
This contains the Dictionary class.

Dictionaries are CSV files, living in the dictionary/ directory. Multiple
dictionaries may apply to a masterfile.

There are two required columns in a dictionary CSV: 'component' and
'short_name' which will both be used to validate the columns in the
masterfile data files. Other columns will be added to the metadata in
masterfiles' columns, as so:

Dictionary:

component,short_name,contact,long_name
timepoint,t1,,Time 1
measure,ourMeas,Jordan Smith,Our Measure


Results in masterfile annotation:
>>> mf.df.t1_ourMeas.long_name
{
    't1': 'Time 1',
    'ourMeas': 'Our Measure'
}
>>> mf.df.t1_ourMeas.contact
{
    'ourMeas': 'Jordan Smith'
}
"""

from __future__ import absolute_import, unicode_literals

from os import path
from glob import glob

import pandas as pd

from . import errors
import attr

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

INDEX_COLS = ['component', 'short_name']


@attr.s
class Dictionary(object):

    mf = attr.ib()

    components = attr.ib()

    dictionary_path = attr.ib(default=None)

    error_list = attr.ib(default=attr.Factory(list))

    _candidate_files = attr.ib(default=attr.Factory(list))

    _loaded_files = attr.ib(default=attr.Factory(list))

    _unprocessed_dataframes = attr.ib(default=attr.Factory(list))

    _loaded_dataframes = attr.ib(default=attr.Factory(list))

    _dataframe = attr.ib(default=None)

    @property
    def dataframe(self):
        if self._dataframe is not None:
            return self._dataframe
        if len(self._loaded_dataframes) > 0:
            self._dataframe = pd.concat(self._loaded_dataframes, sort=True)
        else:
            self._dataframe = pd.DataFrame()
        return self._dataframe

    @property
    def df(self):
        return self.dataframe

    @property
    def columns(self):
        return self.dataframe.columns

    @classmethod
    def load_for_masterfile(klass, mf):
        if mf.root_path is None:
            logger.debug("Trying to load a dictionary with no root_path")
            return None
        dictionary_path = path.join(mf.root_path, 'dictionary')
        d = klass(mf, mf.components, dictionary_path)
        d._find_candidate_files()
        d._read_unprocessed_dataframes()
        d._process_dataframes()
        return d

    def __getitem__(self, key):
        return self.df.loc[key]

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def annotations_for(self, component, value):
        """
        Return all non-empty annotations for a component and value as a dict.
        Empty annotations are filtered out which may result in an empty dict.
        """
        try:
            data = self[component, value]
        except KeyError:
            return {}
        return data.dropna().to_dict()

    def _find_candidate_files(self):
        self._candidate_files = glob(path.join(self.dictionary_path, '*csv'))
        logger.debug(
            'found dictionary files: {}'.format(self._candidate_files))

    def _read_unprocessed_dataframes(self):
        from masterfile import masterfile
        self._unprocessed_dataframes = []
        for f in self._candidate_files:
            df = None
            try:
                df = masterfile.read_csv_no_alterations(f)
            except IOError as e:
                self.error_list.append(errors.FileReadError(
                    locations=[errors.Location(f)],
                    message='unable to read dictionary file {}'.format(f),
                    root_exception=e
                ))
            self._unprocessed_dataframes.append(df)

    def _process_dataframes(self):
        for f, udf in zip(self._candidate_files, self._unprocessed_dataframes):
            try:
                df = udf.set_index(INDEX_COLS)
                df.sort_index(level=INDEX_COLS, inplace=True)
                self._loaded_dataframes.append(df)
                self._loaded_files.append(f)
            except LookupError as e:
                logger.debug("can't find dictionary index in {}".format(f))
                self.error_list.append(errors.DictionaryIndexNotFoundError(
                    locations=[f],
                    message='unable to find dictionary index {}'.format(
                        INDEX_COLS),
                    root_exception=e
                ))
