# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:00:48 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from DSR import ph_dsr

# class Test_DSR:

#     data = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name='testdata_multiarea')
#     results = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name='testresults_DSR')\
#         .drop('statistic', axis=1).astype({'Total Count':'float64'})  
#     ref_data = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name='testdata_1976').astype({'count':'float64'})  
    
#     cols_95 = [0,1,2,3,4,5,8]
    
#     def test_esp_and_NAs(self):
#         df = ph_dsr(self.data, 'count', 'pop', 'ageband', group_cols='area').drop(['Confidence', 'Statistic'], axis=1)
#         assert_frame_equal(df, self.results.iloc[4:7, self.cols_95].reset_index(drop=True))
    
#     def test_2cis(self):
#         df = ph_dsr(self.data, 'count', 'pop', 'ageband', group_cols='area', confidence = [0.95, 0.998]).drop(['Confidence', 'Statistic'], axis=1)
#         assert_frame_equal(df, self.results.iloc[4:7, :].reset_index(drop=True))
    
#     def test_ref_denom_col(self):
#         df = ph_dsr(self.ref_data, 'count', 'pop', 'esp1976', euro_standard_pops = False).drop(['Confidence', 'Statistic'], axis=1)
#         assert_frame_equal(df.astype({'Total Count':'float64'}), 
#                            self.results.iloc[7:8, self.cols_95].drop('area', axis=1).reset_index(drop=True))
    
#     def test_ref_df(self):
#         df = ph_dsr(self.ref_data, 'count', 'pop', 'esp1976', euro_standard_pops=False, 
#                     ref_df = self.ref_data, ref_join_left = 'Age Band', ref_join_right = 'Age Band')\
#             .drop(['Confidence', 'Statistic'], axis=1)
#         assert_frame_equal(df.astype({'Total Count':'float64'}), 
#                            self.results.iloc[7:8, self.cols_95].drop('area', axis=1).reset_index(drop=True))
    
#     def test_multiplier(self):
#         df = ph_dsr(self.data, 'count', 'pop', 'ageband', group_cols = 'area', multiplier = 10000).drop(['Confidence', 'Statistic'], axis=1)
#         assert_frame_equal(df, self.results.iloc[:3, self.cols_95].reset_index(drop=True))
