# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from __future__ import absolute_import, unicode_literals

from os import path
import json
from glob import glob

import pandas as pd

from .vendor import attr
from . import errors


def load(path):
    return Masterfile.load_path(path)


@attr.s
class Masterfile(object):

    # The name of the column with participant identifiers.
    # Generally read from settings.json
    index_column = attr.ib(default=None)

    # The set of components of column names - for example, things such as
    # modality, timepoint, and measure name.
    # Generally read from settings.json
    components = attr.ib(default=None)

    # The path of the masterfile. Must contain a settings.json file.
    root_path = attr.ib(default=None)

    # A list of errors that occurred while trying to read the data. Note that
    # this is not a full-scale validation of the masterfile data, just the
    # things we can't avoid finding while loading the data.
    errors = attr.ib(default=attr.Factory(list))

    # _dataframes and _loaded_data_files will be the same length.
    # The items in _dataframes will have index set to index_column and may
    # have their column types detected.
    _dataframes = attr.ib(default=attr.Factory(list))

    # All files that were successfully loaded.
    _loaded_data_files = attr.ib(default=attr.Factory(list))

    # _unprocessed_dataframes and _candidate_data_files will be the same
    # length.
    # If a candidate file can't be loaded at all, the unprocessed dataframe
    # for the file will be None.
    # dtype for unprocessed dataframes is always str, to avoid dataloss.
    _unprocessed_dataframes = attr.ib(default=attr.Factory(list))

    # All filenames we're going to try to load.
    _candidate_data_files = attr.ib(default=attr.Factory(list))

    _dictionaries = attr.ib(default=attr.Factory(list))

    # Everything in _dataframes, joined by pandas.concat. This is the
    # cached copy.
    # Accessed by the "dataframe" or "df" properties.
    __joined_data = attr.ib(default=None)

    @property
    def dataframe(self):
        if self.__joined_data is not None:
            return self.__joined_data
        self.__joined_data = pd.concat(
            self._dataframes,
            axis='columns',
            join='outer')
        self.__joined_data.index.name = self.index_column
        return self.__joined_data

    @property
    def df(self):
        return self.dataframe

    @classmethod
    def load_path(klass, root_path):
        """
        Initialize a Masterfile from root_path/settings.json, load all .csv
        data and dictionaries into it.
        """
        json_data = None
        settings_file = klass._settings_filename(root_path)
        try:
            json_data = klass._read_settings_json(settings_file)
            mf = klass(**json_data)
            mf._find_and_load_files()
            return mf

        except IOError as e:
            mf = klass()
            mf.errors.append(errors.FileReadError(
                location=settings_file,
                message="Can't read settings file",
                root_exception=e))
            return mf
        except ValueError as e:
            mf = klass()
            mf.errors.append(errors.JSONError(
                location=settings_file,
                message="JSON reading error",
                root_exception=e))
            return mf

    @classmethod
    def _settings_filename(klass, root_path):
        return path.join(str(root_path), "settings.json")

    @classmethod
    def _read_settings_json(klass, filename):
        """
        load root_path/settings.json, parse it, and return a dict with its
        contents.
        """
        data = json.load(open(filename, 'r'))
        data['root_path'] = path.dirname(filename)
        return data

    def _find_and_load_files(self):
        self.errors = []
        self._find_candidate_data_files()
        self._read_unprocessed_data_files()
        self._process_dataframes()

    def _find_candidate_data_files(self):
        root = str(self.root_path)
        self._candidate_data_files = glob(path.join(root, "*csv"))

    def _read_unprocessed_data_files(self):
        self._unprocessed_dataframes = []
        for f in self._candidate_data_files:
            df = None
            try:
                df = pd.read_csv(f, dtype=str)
            except IOError as e:
                self.errors.append(errors.FileReadError(
                    location=f,
                    message="Can't read {}".format(f),
                    root_exception=e
                ))
            self._unprocessed_dataframes.append(df)

    def _process_dataframes(self):
        self._dataframes = []
        self._loaded_data_files = []
        self.__joined_data = None
        for f, udf in zip(
                self._candidate_data_files, self._unprocessed_dataframes):
            try:
                df = udf.set_index(self.index_column)
                self._dataframes.append(df)
            except LookupError as e:
                self.errors.append(errors.IndexNotFoundError(
                    location=f,
                    message="Can't set index column to {}".format(
                        self.index_column),
                    root_exception=e
                ))

    def _read_data_csv(self, filename):
        df = pd.read_csv(
            filename,
            index_col=False,
            dtype={self.index_column: str})
        return df

    def _load_dictionary_csv(self, filename):
        df = pd.read_csv(filename, index_col=False, dtype=str)
        return df
