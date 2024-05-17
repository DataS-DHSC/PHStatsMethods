# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:49:06 2024

@author: Annabel.Westermann
"""

import pandas as pd
import numpy as np
from .confidence_intervals import byars_lower, byars_upper
from .validation import metadata_cols, ci_col, validate_data, format_args


def ph_rate(df, num_col, denom_col, group_cols = None, metadata = True, confidence = 0.95, multiplier = 100000):
    """
    Calculates rates uwith confidence limits using byars or exact method.
    
    Args:
        df: dataframe containing the data to calculate rates for.
        num_col (str): name of the column containing the observed number of cases in the sample(numerator).
        denom_col (str): name of the column containing the number of cases in the sample(denominator).
        group_cols (str | list): A string or list of column name(s) to group the data by. 
                Defaults to None.
        metadata (bool): Whether to include information on the statistic and confidence interval methods.
        confidence (float): Confidence interval(s) to use, either as a float, list of float values or None.
                Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).
        multiplier (int): multiplier for calculation, defualt is 100000 for rates per 100000
    
    Returns: 
        DataFrame with calculated rates and confidence intervals (df).

    """
    
    # Check data and arguments
    confidence, group_cols = format_args(confidence, group_cols)
    df = validate_data(df, num_col, group_cols, metadata, denom_col)
    
    if not isinstance(multiplier, int) or multiplier <= 0:
        raise ValueError("'Multiplier' must be a positive integer")
    
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
        
    if group_cols == ['ph_pkg_group']:
        df = df.drop(columns='ph_pkg_group') 
    
    return df 
