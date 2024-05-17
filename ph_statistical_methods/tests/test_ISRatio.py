# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:44:09 2024

@author: Karandeep.Kaur
"""
import pytest
import pandas as pd
from pathlib import Path
from pandas.testing import assert_frame_equal

from ..ISRatio import ph_ISRatio

class TestISRatio:
    
    path = Path(__file__).parent / 'test_data/testdata_DSR_ISR.xlsx'
    
    # Import data - remove last Multiplier column as not a function output - just used for Excel calculation
    data = pd.read_excel(path, sheet_name = 'testdata_multiarea_isr')
    data_ref = pd.read_excel(path, sheet_name = 'refdata')
    data_results = pd.read_excel(path, sheet_name = 'testresults_ISR')\
        .drop(['ref_rate'], axis=1).astype({'Observed':'float64'})  
    data_obs = pd.read_excel(path, sheet_name = 'testdata_multiarea_lookup')
    
    cols_95 = [0,1,2,3,4,5,8,9]
    
    def test_ownref_2cis(self):
        df = ph_ISRatio(self.data, 'count', 'pop', 'refcount', 'refpop', group_cols = 'area',
                               confidence=[0.95,0.998], refvalue=1).drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[6:9, :].reset_index(drop=True))
        
        
    def test_ownref(self):
        df = ph_ISRatio(self.data, 'count', 'pop', 'refcount', 'refpop', 
                               group_cols = 'area', refvalue=1).drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[6:9, self.cols_95].reset_index(drop=True))


    def test_ownref_refval_2cis(self):
        df = ph_ISRatio(self.data, 'count', 'pop', 'refcount' , 'refpop', group_cols = 'area',
                               confidence=[0.95,0.998], refvalue=100).drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[9:12, :].reset_index(drop=True))     
    
    
    def test_ownref_refval(self):
        df = ph_ISRatio(self.data, 'count', 'pop', 'refcount', 'refpop', group_cols = 'area',
                               confidence=0.95, refvalue=100).drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[9:12, self.cols_95].reset_index(drop=True))        
        
        
    def test_ref_df(self):
        df = ph_ISRatio(self.data.drop(['refcount', 'refpop'], axis=1), 'count', 'pop', 'refcount', 
                               'refpop', group_cols = 'area', refvalue = 1, ref_df = self.data_ref, 
                               ref_join_left = 'ageband', ref_join_right = 'Age Band').drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[6:9, self.cols_95].reset_index(drop=True)) 
        
        
    def test_obs(self):
        df = ph_ISRatio(self.data.drop(['count'], axis=1), 'total_count',  'pop', 'refcount' , 'refpop', 
                               group_cols = 'area', obs_df = self.data_obs, obs_join_left = 'area', 
                               obs_join_right = 'area').drop(['Confidence'], axis=1).astype({'Observed':'float64'})  

        assert_frame_equal(df, self.data_results.iloc[6:9, self.cols_95].reset_index(drop=True))  



    


