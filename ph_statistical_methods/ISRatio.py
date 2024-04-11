# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 14:17:52 2024

@author: Annabel.Westermann
"""

import pandas as pd

from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, format_args, validate_data

df = pd.DataFrame({'area': ['area1', 'area2', 'area3', 'area4'] * 2,
                   'sex': ['Male']*4 + ['Female']*4,
                  #'num': [800, 900, 500, 300, 400, 300, 450, 550],
                  'denom': [1000, 1200, 1000, 500, 800, 400, 900, 800]})

ref_df = pd.DataFrame({'sex':['Male', 'Female'],
                    'num_ref':[10000, 10050],
                    'denom_ref':[200000, 200100]})

num_df = pd.DataFrame({'sex': ['Male', 'Female'],
                       'obs': [1000,  5000]})

group_cols = ['sex']

def calculate_ISRatio(df, num_col, denom_col, ref_num_col, ref_denom_col, group_cols = None, 
                      ref_df = None, num_df = None, metadata = True, confidence = 0.95, refvalue = 1):
    
    # various checks....
    confidence, group_cols = format_args(confidence, group_cols)
    
    # add reference data
    if ref_df is not None:
        df = df.merge(ref_df, how = 'left', on = group_cols)
    
    df['exp_x'] = df[ref_num_col].fillna(0) / df[ref_denom_col] * df[denom_col].fillna(0)
    
    df2 = df.groupby(group_cols)['exp_p'].apply(lambda x: x.sum(skipna=False)).reset_index().rename(columns={'exp_x':'Expected'})
    
    if num_df is not None:
        obs = num_df.groupby(group_cols)[num_col].sum().reset_index().rename(columns={num_col:'Observed'})
    else:
        obs = df.groupby(group_cols)[num_col].sum().reset_index().rename(columns={num_col:'Observed'})
    
    # TODO: might not be merging on all group cols?
    df2 = df2.merge(obs, how = 'left', on = group_cols)
    
    for c in confidence:
        df[ci_col(c, 'lower')] = df.apply(lambda x: byars_lower(x['Observed'], (1-c)), axis=1) / df['Expected'] * refvalue
        df[ci_col(c, 'upper')] = df.apply(lambda x: byars_upper(x['Observed'], (1-c)), axis=1) / df['Expected'] * refvalue
        