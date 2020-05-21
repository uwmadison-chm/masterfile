# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ._metadata import (  # noqa: F401
    version as __version__,
    author as __author__,
    email as __email__
)

__package_version__ = 'masterfile {}'.format(__version__)

from .masterfile import load  # noqa: F401
