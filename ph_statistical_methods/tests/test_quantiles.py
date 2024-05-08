# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:52:40 2024

@author: Hadley.Nanayakkara
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from quantiles import ph_quantile

# Functionality Testing ----------------------------------------------------------------------------
class TestQuantiles:
    
    ## Pytest skips classes with __init__ so simply declare class variables rather than create class attributes
    ## more info: https://pynative.com/python-class-variables/
    
    # Import data - remove last Multiplier column as not a function output - just used for Excel calculation
    data = pd.read_excel('tests/test_data/testdata_Quantiles.xlsx')

    def test_default(self):
        df = self.data[(self.data['GroupSet'] == 'None')]
        assert_frame_equal(
            ph_quantile(df, 'Value').loc[:, ['AreaCode', 'quantile']],
            df.rename(columns={'QuantileInGrp':'quantile'}).loc[:, ['AreaCode', 'quantile']])
        
    @pytest.mark.filterwarnings('ignore::UserWarning') # NA's in quantiles 
    def test_grps(self):
        df = self.data[(self.data['GroupSet'] == 'IndSexReg') & (self.data['IndSexRef'] == '40501Female')]
        assert_frame_equal(
            ph_quantile(df, 'Value', ['ParentCode']).loc[:, ['AreaCode', 'quantile']],
            df.rename(columns={'QuantileInGrp':'quantile'}).loc[:, ['AreaCode', 'quantile']])
    
    @pytest.mark.filterwarnings('ignore::UserWarning')
    def test_invert(self):
        df = self.data[(self.data['GroupSet'] == 'IndSexReg') & (self.data['IndSexRef'] == '90366Female')]
        assert_frame_equal(
            ph_quantile(df, 'Value', ['ParentCode'], invert=False).loc[:, ['AreaCode', 'quantile']],
            df.rename(columns={'QuantileInGrp':'quantile'}).loc[:, ['AreaCode', 'quantile']])
    
    def test_nquantiles(self):
        df = self.data[(self.data['GroupSet'] == 'IndSex') & (self.data['IndSexRef'] == '40501Female')]
        assert_frame_equal(
            ph_quantile(df, 'Value', nquantiles=7).loc[:, ['AreaCode', 'quantile']],
            df.rename(columns={'QuantileInGrp':'quantile'}).loc[:, ['AreaCode', 'quantile']])
    
    @pytest.mark.filterwarnings('ignore::UserWarning')
    def test_invert_nquantiles(self):
        df = self.data[(self.data['GroupSet'] == 'IndSex') & (self.data['IndSexRef'] == '90366Female')]
        assert_frame_equal(
            ph_quantile(df, 'Value', nquantiles=7, invert=False).loc[:, ['AreaCode', 'quantile']],
            df.rename(columns={'QuantileInGrp':'quantile'}).loc[:, ['AreaCode', 'quantile']])
        
    def test_warning(self):
        with pytest.warns(UserWarning):
            df = self.data[(self.data['GroupSet'] == 'IndSexReg') & (self.data['IndSexRef'] == '40501Female')]
            ph_quantile(df, 'Value').loc[:, ['AreaCode', 'quantile']]
        


# Error Handling -----------------------------------------------------------------------------------

class TestQuantilesErrors:

    df = pd.DataFrame({'val': [None, 82, 9, 48, 65, 8200, 10000, 10000, 8, 7, 750, 900],
                       'groups': ['Group1', 'Group2','Group3'] * 4,})

    # No test needed for group_cols because it will always be converted to a list.
    
    def test_values_er(self):
        with pytest.raises(TypeError, match = "Pass 'values' as a string"):
            ph_quantile(self.df, 50)

    def test_nquantiles_er(self):
        with pytest.raises(TypeError, match = "Pass 'nquantiles' as a integer"):
            ph_quantile(self.df, 'val', nquantiles = "10")

    def test_invert_er(self):
        with pytest.raises(TypeError, match = "Pass 'invert' as a boolean"):
            ph_quantile(self.df, 'val', invert = "True")

    # Other error handling tests are covered in test_validation.py