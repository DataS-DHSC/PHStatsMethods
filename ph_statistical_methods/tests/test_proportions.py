# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 17:07:04 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
from pathlib import Path
from pandas.testing import assert_frame_equal

from ..proportions import ph_proportion


class TestProportions:
    
    ## Pytest skips classes with __init__ so simply declare class variables rather than create class attributes
    ## more info: https://pynative.com/python-class-variables/

    # Import data - remove last Multiplier column as not a function output - just used for Excel calculation
    path = Path(__file__).parent / 'test_data/testdata_Proportion.xlsx'
    
    data = pd.read_excel(path, sheet_name = 'testdata_Prop').iloc[:,:-1]
    data_group = pd.read_excel(path, sheet_name = 'testdata_Prop_g').iloc[:,:-1]
    
    # Columns for 95% CI, so dropping 99.8% and Confidence column containing '95%, 99.8%'
    cols_95 = [0,1,2,3,4,5,8,10]
        
    @pytest.mark.parametrize('multiplier', [(-10), (1.5)])
    def test_multiplier_error(self, multiplier):
        with pytest.raises(ValueError, match="'Multiplier' must be a positive integer"):
            ph_proportion(self.data, 'Numerator', 'Denominator', multiplier = multiplier)

    def test_default(self):
        df = ph_proportion(self.data.iloc[:8, :3], 'Numerator', 'Denominator').drop(['Confidence'], axis=1)
        assert_frame_equal(df, self.data.iloc[:8, self.cols_95])
    
    def test_2ci(self):
        df = ph_proportion(self.data.iloc[:8, :3], 'Numerator', 'Denominator', confidence = [0.95, 0.998])
        assert_frame_equal(df, self.data.iloc[:8, :])
        
    def test_percentage(self):
        df = ph_proportion(self.data.iloc[8:16, :3], 'Numerator', 'Denominator', multiplier = 100)\
            .drop(['Confidence'], axis=1)
        assert_frame_equal(df, self.data.iloc[8:16, self.cols_95])
        
    def test_NAs(self):
        df = ph_proportion(self.data.iloc[16:, :3], 'Numerator', 'Denominator').drop(['Confidence'], axis=1)
        assert_frame_equal(df, self.data.iloc[16:, self.cols_95])
        
    def test_group(self):
        df = ph_proportion(self.data, 'Numerator', 'Denominator', group_cols = 'Area')
        assert_frame_equal(df, self.data_group)
    
