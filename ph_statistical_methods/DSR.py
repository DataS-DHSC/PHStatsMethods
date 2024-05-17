# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from math import sqrt

from .utils import join_euro_standard_pops
from .confidence_intervals import dobson_lower, dobson_upper
from .validation import format_args, validate_data, check_kwargs, ci_col, metadata_cols


def ph_dsr(df, num_col, denom_col, ref_denom_col, group_cols = None, metadata = True, 
           confidence = 0.95, multiplier = 100000, euro_standard_pops = True, **kwargs):
    
    """Calculates directly standardised rates with confidence limits using Byar's
    method (1) with Dobson method adjustment (2).
    
    Args:
        df: DataFrame containing the data to be standardised.
        
        num_col (str): column name from data containing the observed number of events for
        each standardisation category (e.g. ageband) within each grouping set (e.g. area).
        
        denom_col (str): column name from data containing the population for each standardisation 
        category (e.g. age band).
        
        ref_denom_col (str): the standard populations for each standardisation category (e.g. age band).
        This is either the column name in the main dataframe, the reference data if given, or the column
        name of the agebands to join to if `euro_standard_pops` is set to True. 
        
        group_cols: A string or list of column name(s) to group the data by. Default to None.

        metadata (bool): Whether to include information on the statistic and confidence interval methods.
        
        euro_standard_pops (bool): Whether to use the european standard populations.
        You can see what these populations are with `euro_standard_pop()`.
        
        multiplier (int): the multiplier used to express the final values. Default 100,000.
        
        confidence (float): Confidence interval(s) to use, either as a float, list of float values or None.
        Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).
        
    **kwargs:
        ref_df: DataFrame of reference data to join.
        
        ref_join_left: A string or list of column name(s) in `df` to join on to.
        
        ref_join_right: A string or list of column name(s) in `ref_df` to join on to.
        
    Returns:
        DataFrame of calculated rates and confidence intervals
        
    References:
        (1) Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort studies. 
        Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
        (2) Dobson A et al. Confidence intervals for weighted sums of Poisson parameters. Stat Med 1991;10:457-62.

    """

    df = df.copy().reset_index(drop=True)
    
    if not isinstance(multiplier, int) or multiplier <= 0:
        raise ValueError("'Multiplier' must be a positive integer")
    
    # Get ref_denom_col for validation checks from ESP data if True - do it before check_kwargs so can test if ref_denom_col is numeric there
    if euro_standard_pops:
        df = join_euro_standard_pops(df, ref_denom_col, group_cols)
        ref_denom_col = 'euro_standard_pops'
        
    confidence, group_cols = format_args(confidence, group_cols)
    ref_df, ref_join_left, ref_join_right = check_kwargs(df, kwargs, 'ref', ref_denom_col)
    df = validate_data(df, num_col, group_cols, metadata, denom_col, ref_df = ref_df)
        
    if ref_df is not None and euro_standard_pops == False:
        df = df.merge(ref_df, how = 'left', left_on = ref_join_left, right_on = ref_join_right).drop(ref_join_right, axis=1)
        
    df['wt_rate'] = df[num_col].fillna(0) * df[ref_denom_col] / df[denom_col]
    df['sq_rate'] = df[num_col].fillna(0) * (df[ref_denom_col] / df[denom_col])**2
    
    df = df.groupby(group_cols).agg({num_col: 'sum', 
                                      denom_col: lambda x: x.sum(skipna=False), 
                                      'wt_rate': lambda x: x.sum(skipna=False),
                                      ref_denom_col: lambda x: x.sum(skipna=False), 
                                      'sq_rate': lambda x: x.sum(skipna=False)}).reset_index()

    df['Value'] = df['wt_rate'] / df[ref_denom_col] * multiplier
    df['vardsr'] = 1 / df[ref_denom_col]**2 * df['sq_rate']
    
    if confidence is not None:
        for c in confidence:
            df[ci_col(c, 'lower')] = df.apply(lambda x: dobson_lower(x['Value'], x[num_col], x['vardsr'], c, multiplier), axis=1)
            df[ci_col(c, 'upper')] = df.apply(lambda x: dobson_upper(x['Value'], x[num_col], x['vardsr'], c, multiplier), axis=1)
    
    # Tidy dataframe
    df = df.drop(['vardsr', 'wt_rate', 'sq_rate', ref_denom_col], axis=1).rename(columns={num_col: 'Total Count', denom_col: 'Total Pop'})
    df.loc[df['Total Count'] < 10, 'Value'] = np.nan
    
    if metadata:
        df = metadata_cols(df, f'DSR per {multiplier}', confidence, 'Dobson')
    
    if group_cols == ['ph_pkg_group']:
        df = df.drop(columns='ph_pkg_group') 
            
    return df
        
        