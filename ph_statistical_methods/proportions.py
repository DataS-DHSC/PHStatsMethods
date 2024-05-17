# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 16:52:40 2024

@author: Annabel.Westermann
"""

import pandas as pd

from .confidence_intervals import wilson_lower, wilson_upper
from .validation import metadata_cols, ci_col, format_args, validate_data


def ph_proportion(df, num_col, denom_col, group_cols = None, metadata = True, confidence = 0.95, multiplier = 1):
    """Calculates proportions with confidence limits using Wilson Score method.

    Args:
        df: DataFrame containing the data to calculate proportions for.
        num_col (str): Name of column containing observed number of cases in the sample
                (the numerator of the population).
        denom_col (str): Name of column containing number of cases in sample 
                (the denominator of the population).
        group_cols (str | list): A string or list of column name(s) to group the data by. 
                Defaults to None.
        metadata (bool): Whether to include information on the statistic and confidence interval methods.
        confidence (float): Confidence interval(s) to use, either as a float, list of float values or None.
                Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).
        multiplier (int): multiplier used to express the final values (e.g. 100 = percentage)

    Returns:
        DataFrame of calculated proportion statistics with confidence intervals (df).
        
    """

    # Ensure original df remains unchanged 
    df = df.copy()

    # Check data and arguments
    confidence, group_cols = format_args(confidence, group_cols)
    df = validate_data(df, num_col, group_cols, metadata, denom_col)
        
    if not isinstance(multiplier, int) or multiplier <= 0:
        raise ValueError("'Multiplier' must be a positive integer")
      
    if (df[num_col] > df[denom_col]).any():
        raise ValueError('Numerators must be less than or equal to the denominator for a proportion statistic')   
    
    # Sum Numerator and Denominator columns, ensure NAs are included. 
    df = df.groupby(group_cols)[[num_col, denom_col]].apply(lambda x: x.sum(skipna=False)).reset_index()

    ### Calculate statistic
    df['Value'] = (df[num_col] / df[denom_col]) * multiplier

    if confidence is not None:
        for c in confidence:
            df[ci_col(c, 'lower')] = df.apply(lambda y: wilson_lower(y[num_col], y[denom_col], c),
                                                axis=1) * multiplier
            df[ci_col(c, 'upper')] = df.apply(lambda y: wilson_upper(y[num_col], y[denom_col], c),
                                                axis=1) * multiplier
            
    if metadata:
        statistic = 'Percentage' if multiplier == 100 else f'Proportion of {multiplier}'
        df = metadata_cols(df, statistic, confidence, 'Wilson')
        
    if group_cols == ['ph_pkg_group']:
        df = df.drop(columns='ph_pkg_group') 
        
    return df
