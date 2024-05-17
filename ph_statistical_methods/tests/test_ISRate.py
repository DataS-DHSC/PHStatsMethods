# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:50:05 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
from pathlib import Path
from pandas.testing import assert_frame_equal

from ..ISRate import ph_ISRate


class TestISRate:
    
    path = Path(__file__).parent / 'test_data/testdata_DSR_ISR.xlsx'
    
    data = pd.read_excel(path, sheet_name = 'testdata_multiarea_isr')
    results = pd.read_excel(path, sheet_name = 'testresults_ISR')
    test_ISR_lookup = pd.read_excel(path, sheet_name = 'testdata_multiarea_lookup')
    test_ISR_refdata = pd.read_excel(path, sheet_name = 'refdata')
    test_err2 = pd.read_excel(path, sheet_name = 'testdata_err2')

    def test_default(self):
            df = ph_ISRate(self.data, 'count', 'pop', 'refcount', 'refpop', group_cols='area').iloc[:, :7]
            assert_frame_equal(df, self.results.iloc[:3, :7], check_dtype=False)

    def test_default_obs_total(self):
            df = ph_ISRate(self.data, 'total_count', 'pop', 'refcount', 'refpop', group_cols='area', confidence=[0.95, 0.998],
                                  obs_df = self.test_ISR_lookup, obs_join_left = 'area', obs_join_right = 'area').iloc[:, :10]
            assert_frame_equal(df, self.results.iloc[:3, :10], check_dtype=False)

    def test_default_ref(self):
            df = ph_ISRate(self.data.drop(columns=['refcount', 'refpop']), 'count', 'pop', 'refcount', 'refpop', group_cols='area',
                                  ref_df = self.test_ISR_refdata, ref_join_left = 'ageband', ref_join_right = 'Age Band').iloc[:, :7]
            assert_frame_equal(df, self.results.iloc[:3, :7], check_dtype=False)

    def test_zero_pop(self):
            df = ph_ISRate(self.test_err2, 'count', 'pop', 'refcount', 'refpop', group_cols='area',
                                  ref_df = self.test_ISR_refdata, ref_join_left = 'ageband', ref_join_right = 'Age Band').iloc[:, :7].reset_index(drop=True)
            assert_frame_equal(df, self.results.iloc[12:14, :7].reset_index(drop=True), check_dtype=False)

    def test_multiplier(self):
            df = ph_ISRate(self.data, 'count', 'pop', 'refcount', 'refpop', group_cols='area', multiplier=1000).iloc[:, :7].reset_index(drop=True)
            assert_frame_equal(df, self.results.iloc[3:6, :7].reset_index(drop=True), check_dtype=False)

