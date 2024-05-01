# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:49:06 2024

@author: Annabel.Westermann
"""

import pandas as pd
import numpy as np
from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data, format_args


def ph_rate(df, num_col, denom_col, group_cols = None, metadata = True, confidence = 0.95, multiplier = 100000):
    """
    Calculates rates uwith confidence limits using byars or exact method.
    
    Args:
        df: dataframe containing the data to calculate rates for.
        num_col: (str): name of the column containing the observed number of cases in the sample(numerator).
        denom_col: (str): name of the column containing the number of cases in the sample(denominator).
        type: select which data you would like to return. "lower" is lower cl, "upper" is upper cl, "value" is value,
                 "standard" is value, lowercl, and uppercl, "full" is the default that will return all data.
        confidence: confidence level used for calculation, default is 0.95 for 95% confidence levels.
        multiplier: multiplier for calculation, defualt is 100000 for rates per 100000
    
    Returns: 
        dataframe with calculated rates and confidence intervals.

    """
    
    # Check data and arguments
    confidence, group_cols = format_args(confidence, group_cols)
    validate_data(df, num_col, group_cols, metadata, denom_col)
    
    if not isinstance(multiplier, int) or multiplier <= 0:
        raise ValueError("'Multiplier' must be a positive integer")
    
    if group_cols is not None:
        df = df.groupby(group_cols)[[num_col, denom_col]].apply(lambda x: x.sum(skipna=False)).reset_index()
        
    #calculate value column
    df['Value'] = df[num_col] / df[denom_col] * multiplier
    
   #calculate confidence intervals
    if confidence is not None:
        for c in confidence:
            df[ci_col(c, 'lower')] = df.apply(lambda y: byars_lower(y[num_col], c), axis=1) / df[denom_col] * multiplier
            df[ci_col(c, 'upper')] = df.apply(lambda y: byars_upper(y[num_col], c), axis=1) / df[denom_col] * multiplier
          
    # Generate statistic and method columns
    if metadata:
        method = np.where(df[num_col] < 10, 'Exact', 'Byars')
        df = metadata_cols(df, f'Rate per {multiplier}', confidence, method)
    
    return df 
