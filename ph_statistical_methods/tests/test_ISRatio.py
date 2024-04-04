# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:44:09 2024

@author: Karandeep.Kaur
"""
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from ISRatio import calculate_ISRatio

class TestISRatio:
    
    
    # Import data - remove last Multiplier column as not a function output - just used for Excel calculation
    data = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testdata_multiarea_isr')
    data_ref = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'refdata')
    data_results = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testresults_ISR')
    data_obs = pd.read_excel('tests/test_data/testdata_ISR_obs.xlsx', sheet_name = 'df')
    obs = pd.read_excel('tests/test_data/testdata_ISR_obs.xlsx', sheet_name = 'obs')
    obs_results = pd.read_excel('tests/test_data/testdata_ISR_obs.xlsx', sheet_name = 'obs_results')
    cols_95 = [0,1,2,4,5,6,9,10]
    
    def test_ownref_2cis(self):
        #full output two cis
    
        df = calculate_ISRatio(self.data, "count", "pop", "refcount" , "refpop", group_cols = ["area"],
                               confidence=[0.95,0.998], ref_df=None,refvalue=1, 
                               metadata=True, observed_totals=None).drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[6:9, :].reset_index(drop=True).drop(['ref_rate'],axis=1).astype({"observed":"float64"}))
        
    def test_ownref(self):
        #full output one ci
    
        df = calculate_ISRatio(self.data, "count", "pop", "refcount" , "refpop", group_cols = ["area"],
                               confidence=0.95, ref_df=None, refvalue=1, 
                               metadata=True, observed_totals=None).drop(['Confidence'], axis=1)
        assert_frame_equal(df, self.data_results.iloc[6:9, self.cols_95].reset_index(drop=True).astype({"observed":"float64"})) 

    def test_ownref_refval_2cis(self):
        #full output two cis
    
        df = calculate_ISRatio(self.data, "count", "pop", "refcount" , "refpop", group_cols = ["area"],
                               confidence=[0.95,0.998], ref_df=None, refvalue=100, 
                               metadata=True, observed_totals=None).drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[9:12, :].reset_index(drop=True).drop(['ref_rate'],axis=1).astype({"observed":"float64"}))        
    
    def test_ownref_refval(self):
        #full output  one ci
    
        df = calculate_ISRatio(self.data, "count", "pop", "refcount" , "refpop", group_cols = ["area"],
                               confidence=0.95, ref_df=None, refvalue=100, 
                               metadata=True, observed_totals=None).drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[9:12, self.cols_95].reset_index(drop=True).astype({"observed":"float64"}))        
        
    def test_ref_df(self):
        #full output  one ci
        
    
        df = calculate_ISRatio(self.data, "count", "pop", "refcount" , "refpop", group_cols = ["area"],
                               confidence=0.95, ref_df=self.data_ref, refvalue=1, 
                               metadata=True, observed_totals=None).drop(['Confidence'], axis=1)
        
        assert_frame_equal(df, self.data_results.iloc[6:9, self.cols_95].reset_index(drop=True).astype({"observed":"float64"})) 
        
    def test_obs(self):
        #full output  one ci
        
    
        df = calculate_ISRatio(self.data_obs, "observed", "pop", "refcount" , "refpop", group_cols = ["indicatorid","year","sex"],
                               confidence=0.95, ref_df=None, refvalue=1, 
                               metadata=True, observed_totals=self.obs).drop(['Confidence'], axis=1)

        assert_frame_equal(df, self.obs_results.drop(['Confidence'], axis=1))#.astype({"observed":"float64"}))  



    


