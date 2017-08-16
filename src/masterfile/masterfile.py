# -*- coding: utf-8 -*-

"""
"""

from itertools import chain

import pandas as pd

from .vendor import attr
from .errors import Error


@attr.s
class Masterfile(object):

    index_column = attr.ib()

    components = attr.ib()

    _dataframes = attr.ib(default=attr.Factory(list))

    errors = attr.ib(default=attr.Factory(list))

    @classmethod
    def load_path(klass, pathname):
        """
        Initialize a Masterfile from pathname/settings.json, load all .csv
        data and dictionaries into it.
        TODO: Implement this.
        """
        pass

    def _add_csv_files_to_dataframes(self, filenames):
        dataframes, errors = self._load_csv_files(filenames)
        self._dataframes = list(chain(self._dataframes, dataframes))
        self.errors = list(chain(self.errors, errors))

    def _load_data_files(self, filenames):
        dataframes = []
        errors = []
        for f in filenames:
            try:
                df = self._load_csv(f)
                dataframes.append(df)
            except LookupError as e:
                errors.append(Error(
                    code='E101',
                    filename=f,
                    message='column {} not found'.format(self.index_column)))
        return (dataframes, errors)

    def _load_csv(self, filename):
        df = pd.read_csv(
            filename,
            index_col=False,
            dtype={self.index_column: str})
        df.set_index(self.index_column, inplace=True)
        return df
