#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

from os import path
from glob import glob

import pytest

import masterfile

# EXAMPLE_PATH =
# GOOD_PATH =
# GOOD_CSVS = glob(path.join(GOOD_PATH, '*csv'))
# PROBLEMS_PATH = path.join(EXAMPLE_PATH, 'problems')


@pytest.fixture()
def example_path():
    return path.join(path.dirname(path.abspath(__file__)), 'examples')


@pytest.fixture()
def good_path(example_path):
    return path.join(example_path, 'good')


@pytest.fixture()
def good_csvs(good_path):
    return glob(path.join(good_path, '*csv'))


@pytest.fixture()
def problems_path(example_path):
    return path.join(example_path, 'problems')


@pytest.fixture()
def good_mf(good_path):
    return masterfile.masterfile.Masterfile.load_path(good_path)


@pytest.fixture()
def full_good_mf(good_path):
    return masterfile.load(good_path)


@pytest.fixture()
def good_dict(good_mf):
    return masterfile.dictionary.Dictionary.load_for_masterfile(good_mf)


@pytest.fixture()
def good_annotator(good_mf, good_dict):
    return masterfile.annotator.Annotator(good_mf, good_dict)


@pytest.fixture()
def nosettings_mf(example_path):
    return masterfile.masterfile.Masterfile.load_path(example_path)


@pytest.fixture()
def problems_mf(problems_path):
    return masterfile.masterfile.Masterfile.load_path(problems_path)


@pytest.fixture()
def full_problems_mf(problems_path):
    return masterfile.load(problems_path)
