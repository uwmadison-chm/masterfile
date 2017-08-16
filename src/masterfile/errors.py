# -*- coding: utf-8 -*-

"""
"""

from .vendor import attr


@attr.s
class Error(object):

    code = attr.ib()

    filename = attr.ib()

    message = attr.ib()


ERROR_CODES = {
    'E1': 'Columns',
    'E101': 'index column not found',
    'E102': 'duplicate column name'
}
