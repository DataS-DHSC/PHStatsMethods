# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 15:04:04 2024

@author: Jack.Burden_DHSC
"""

import pytest
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal

from ..rates import ph_rate

class Test_rates:
    
    path = Path(__file__).parent / 'test_data/testdata_Rate.xlsx'
    
    data = pd.read_excel(path, sheet_name = 'testdata_Rate').drop('Multiplier', axis=1)
    data_group = pd.read_excel(path, sheet_name = 'testdata_Rate_g').drop('Multiplier', axis=1)
    
    cols_95 = [0,1,2,3,4,5,8,9]
    
    def test_default(self):
        df = ph_rate(self.data.iloc[8:16, :3], 'Numerator', 'Denominator', 'Area').drop(['Confidence'], axis=1)
        assert_frame_equal(df, self.data.iloc[8:16, self.cols_95].reset_index(drop=True))
        
    def test_multiplier(self):
        df = ph_rate(self.data.iloc[:8, :3], 'Numerator', 'Denominator', 'Area', multiplier=100).drop(['Confidence'], axis=1)
        assert_frame_equal(df, self.data.iloc[:8, self.cols_95])
    
    @pytest.mark.parametrize('multiplier', [(-10), (1.5)])
    def test_multiplier_error(self, multiplier):
        with pytest.raises(ValueError, match="'Multiplier' must be a positive integer"):
            ph_rate(self.data, 'Numerator', 'Denominator', multiplier = multiplier)
            
    def test_2ci(self):
         df = ph_rate(self.data.iloc[8:16, :3], 'Numerator', 'Denominator', 'Area', confidence = [0.95, 0.998]).drop(['Confidence'], axis=1)
         assert_frame_equal(df, self.data.iloc[8:16, :].reset_index(drop=True))
         
    def test_NAs(self):
        df = ph_rate(self.data.iloc[16:, :3], 'Numerator', 'Denominator','Area').drop(['Confidence','Method'], axis=1)
        assert_frame_equal(df, self.data.iloc[16:, self.cols_95].drop('Method', axis=1).reset_index(drop=True))
    
    # dropping 'method' column for now while figure out method column
    def test_group(self):
        df = ph_rate(self.data, 'Numerator', 'Denominator', group_cols = 'Area').drop(['Confidence','Method'], axis=1)
        assert_frame_equal(df, self.data_group.drop(['Method','Confidence'], axis=1))
    

