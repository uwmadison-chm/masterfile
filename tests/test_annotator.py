#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/uwmadison-chm/masterfile
# Copyright (c) 2020 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.


class TestAnnotator(object):

    def test_make_annotations_series(self, good_annotator):
        annotations = good_annotator.make_series_annotations('sr_t1_foo_var1')
        assert 'contact' in annotations
        assert annotations['contact']['measure_foo'] == 'Jordan'

    def test_annotate_series(self, good_annotator):
        df = good_annotator.masterfile.df
        s = df.sr_t1_foo_var1
        good_annotator.annotate_series(s)
        assert hasattr(s, 'contact')
        assert s.contact['measure_foo'] == 'Jordan'

    def test_annotates_dataframe(self, good_annotator):
        df = good_annotator.masterfile.df
        good_annotator.annotate_dataframe(df)
        assert df.sr_t1_foo_var1.contact['measure_foo'] == 'Jordan'
        assert df.sr_t1_foo_var1.long_name['measure_foo'] == 'Foo Measure'

    def test_annotates_masterfile(self, good_annotator):
        good_annotator.annotate_masterfile()
        mf = good_annotator.masterfile
        assert mf.df.sr_t1_foo_var1.contact['measure_foo'] == 'Jordan'

    def test_annotation_sets_metadata(self, good_annotator):
        good_annotator.annotate_masterfile()
        df = good_annotator.masterfile.dataframe
        ddict = good_annotator.dictionary
        assert list(df._metadata) == list(ddict.columns)
