# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:49:06 2024

@author: Annabel.Westermann
"""

import pandas as pd
import numpy as np
from .confidence_intervals import byars_lower, byars_upper
from .validation import metadata_cols, ci_col, validate_data, format_args, group_args


def ph_rate(df, num_col, denom_col, group_cols = None, metadata = True, confidence = 0.95, multiplier = 100000):
    """Calculates rates uwith confidence limits using byars or exact method.
    
    Parameters
    ----------
    df
        Dataframe containing the data to calculate rates for.
    num_col : str
        Name of the column containing the observed number of cases in the sample(numerator).
    denom_col : str
        Name of the column containing the number of cases in the sample(denominator).
    group_cols : str | list
        A string or list of column name(s) to group the data by. 
        Defaults to None.
    metadata : bool 
        Whether to include information on the statistic and confidence interval methods.
    confidence : float
        Confidence interval(s) to use, either as a float, list of float values or None.
        Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).
    multiplier : int 
        Multiplier for calculation, default is 100000 for rates per 100,000
    
    Returns
    -------
    Pandas DataFrame
        DataFrame with calculated rates and confidence intervals (df).

    Notes
    -----
    For numerators >= 10 Byar's method (1) is applied using the internal byars_lower and byars_upper
    functions. For small numerators Byar's method is less accurate and so an exact method (2) based 
    on the Poisson distribution is used.

    References
    ----------
    (1) Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis 
        of cohort studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    (2) Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    """
    
    # Check data and arguments
    confidence, group_cols = format_args(confidence, group_cols)
    df = validate_data(df, num_col, group_cols, metadata, denom_col)
    
    if not isinstance(multiplier, int) or multiplier <= 0:
        raise ValueError("'Multiplier' must be a positive integer")
    
    # Grouping by temporary column to reduce duplication in code
    df, group_cols = group_args(df, group_cols, False)

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
