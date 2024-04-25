# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 15:04:04 2024

@author: Jack.Burden_DHSC
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from rates import ph_rate

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