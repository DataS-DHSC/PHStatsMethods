# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 15:04:04 2024

@author: Jack.Burden_DHSC
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from rates import ph_rate



data = pd.read_excel('tests/test_data/testdata_Rate.xlsx', sheet_name = 'testdata_Rate').drop('Multiplier', axis=1)
data_group = pd.read_excel('tests/test_data/testdata_Rate.xlsx', sheet_name = 'testdata_Rate_g').drop('Multiplier', axis=1)

cols_95 = [0,1,2,3,4,5,8,9]

def test_default(data):
    df = ph_rate(data.iloc[8:16, :3], 'Numerator', 'Denominator').drop(['Confidence'], axis=1)
    assert_frame_equal(df, data.iloc[8:16, cols_95])
    
def test_multiplier(data):
    df = ph_rate(data.iloc[:8, :3], 'Numerator', 'Denominator', multiplier=100).drop(['Confidence'], axis=1)
    assert_frame_equal(df, data.iloc[:8, cols_95])

@pytest.mark.parametrize('multiplier', [(-10), (1.5)])
def test_multiplier_error(data, multiplier):
    with pytest.raises(ValueError, match="'Multiplier' must be a positive integer"):
        ph_rate(data, 'Numerator', 'Denominator', multiplier = multiplier)
        
def test_2ci(data):
     df = ph_rate(data.iloc[8:16, :3], 'Numerator', 'Denominator', confidence = [0.95, 0.998]).drop(['Confidence'], axis=1)
     assert_frame_equal(df, data.iloc[8:16, :])
     
def test_NAs():
    df = ph_rate(data.iloc[16:, :3], 'Numerator', 'Denominator').drop(['Confidence'], axis=1)
    assert_frame_equal(df, data.iloc[16:, cols_95])
    
def test_group(data, data_group):
    df = ph_rate(data, 'Numerator', 'Denominator', group_cols = 'Area')
    assert_frame_equal(df, data_group)




class TestRates:
    
    data = pd.read_excel('tests/test_data/testdata_Rate.xlsx', sheet_name = 'testdata_Rate').iloc[:,:-1]
    data_group = pd.read_excel('tests/test_data/testdata_Rate.xlsx', sheet_name = 'testdata_Rate_g').iloc[:,:-1]
    
    cols_95 = [0,1,2,3,4,5,8,10]
    
    def test_default(self):
        df = ph_rate(self.data.iloc[:8, :3], 'Numerator', 'Denominator').drop(['Confidence'], axis=1)
        assert_frame_equal(df, self.data.iloc[:8, self.cols_95])
    
    @pytest.mark.parametrize('multiplier', [(-10), (1.5)])
    def test_multiplier_error(self, multiplier):
        with pytest.raises(ValueError, match="'Multiplier' must be a positive integer"):
            ph_rate(self.data, 'Numerator', 'Denominator', multiplier = multiplier)
            
    def test_2ci(self):
         df = ph_rate(self.data.iloc[:8, :3], 'Numerator', 'Denominator', confidence = [0.95, 0.998])
         assert_frame_equal(df, self.data.iloc[:8, :])
         
    def test_NAs(self):
        df = ph_rate(self.data.iloc[16:, :3], 'Numerator', 'Denominator').drop(['Confidence'], axis=1)
        assert_frame_equal(df, self.data.iloc[16:, self.cols_95])
        
    def test_group(self):
        df = ph_rate(self.data, 'Numerator', 'Denominator', group_cols = 'Area')
        assert_frame_equal(df, self.data_group)