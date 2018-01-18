# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


from masterfile import errors


def validate(masterfile):
    logger.debug("io_validator:validate()")
    errlist = [e for e in masterfile.errors if isinstance(e, errors.IOError)]
    logger.debug("found {} errors".format(len(errlist)))
    return errlist
