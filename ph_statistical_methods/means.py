# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:12:17 2024

@author: Annabel.Westermann
"""

import numpy as np
import pandas as pd
from scipy import stats

from validation import metadata_cols, ci_col, validate_data, format_args

df = pd.DataFrame({'area': ['Area1', 'Area1','Area1','Area2','Area2','Area2'],
                  'num': [20,np.nan,40,200,300,400]})


def ph_mean(df, num_col, group_cols, metadata = True, confidence = 0.95):
    
    # Check data and arguments
    confidence, group_cols = format_args(confidence, group_cols)
    validate_data(df, num_col, group_cols, metadata)
    
    if group_cols is None:
        raise TypeError('group_cols cannot be None for a mean statistic')
        
    # get grouped statistics
    # TODO: multiple lambda not working?
    df = df.groupby(group_cols)[num_col].agg([lambda x: x.sum(skipna=False), 
                                              lambda x: x.count().astype(float), 
                                              lambda x: x.std(skipna=False)]).reset_index()
    
    df = df.rename(columns={df.columns[-3]: 'value_sum', df.columns[-2]: 'value_count', df.columns[-1]: 'stdev'})
    
    df['Value'] = df['value_sum'] / df['value_count']
    
    for c in confidence:
        df[ci_col(c, 'lower')] = df['Value'] - abs(stats.t.ppf((1-c)/2, df['value_count'] - 1)) * df['stdev'] / df['value_count']**.5
        df[ci_col(c, 'upper')] = df['Value'] + abs(stats.t.ppf((1-c)/2, df['value_count'] - 1)) * df['stdev'] / df['value_count']**.5

    if metadata:
        df = metadata_cols(df, "Mean", confidence, "Student's t-distribution")
    
    return df

