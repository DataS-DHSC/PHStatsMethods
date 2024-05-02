# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:49:43 2024

@author: T.Vikneswaran_DHSC
"""

import pandas as pd
import numpy as np

from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data, format_args, check_kwargs


def calculate_ISRate(df, num_col, denom_col, ref_num_col, ref_denom_col, group_cols, 
                     metadata=True, confidence=0.95, refvalue=1, **kwargs):
    
    """Calculates indirectly standardized rates with confidence limits using Byar's or exact CI method.
    
    Args:
        df: DataFrame containing the data to calculate IS rates for.
        
        num_col (str): Field name from data containing the observed number of events for
        each standardisation category within each grouping set.
        
        denom_col (str): Field name from data containing the person-time or population at risk
        for each standardisation category.
        
        ref_num_col (str): The observed number of events in the reference population for
        each standardisation category.
        
        ref_denom_col (str): The person-time or population at risk in the reference population
        for each standardisation category.
        
        group_cols: A string or list of column name(s) to group the data by.
        
        metadata (bool): Whether to include metadata columns. Defaults to True.
        
        confidence (float): Confidence interval(s) to use, either as a float, list of float values
        between 0.9 and 1. Defaults to 0.95 (2 std from mean).
        
        refvalue (int): The standardised reference rate. Default is 1.
        
    **kwargs:
        ref_df
        ref_join_cols
        ref_join_left
        ref_join_right
        obs_df
        obs_join_left
        obs_join_right

    """
    
    # Validate data
    confidence, group_cols = format_args(confidence, group_cols)
    ref_df, ref_join_left, ref_join_right = check_kwargs(df, kwargs, 'ref', ref_num_col, ref_denom_col)
    obs_df, obs_join_left, obs_join_right = check_kwargs(df, kwargs, 'obs', num_col)
    validate_data(df, denom_col, group_cols, metadata, ref_df=ref_df)
    
    if ref_df is not None:
        df = df.merge(ref_df, how='left', left_on=ref_join_left, right_on=ref_join_right).drop(ref_join_right, axis=1)
    
    df['exp_rate'] = df[ref_num_col].fillna(0) / df[ref_denom_col] * df[denom_col].fillna(0)
    
    if obs_df is not None:
        df = df.groupby(group_cols)[['exp_rate']].apply(lambda x: x.sum(skipna=False)).reset_index()
        df = df.merge(obs_df, how='left', left_on=obs_join_left, right_on=obs_join_right)
    else:
        df = df.groupby(group_cols)[['exp_rate', num_col]].sum().reset_index()
        
    df = df.rename(columns={num_col: 'Observed', 'exp_rate': 'Expected'}).reindex(columns=(group_cols + ['Observed', 'Expected']))
    
    df['Rate'] = df['Observed'] / df['Expected'] * refvalue
    
    for c in confidence:
        df[ci_col(c, 'lower')] = df.apply(lambda x: byars_lower(x['Observed'], c), axis=1) / df['Expected'] * refvalue
        df[ci_col(c, 'upper')] = df.apply(lambda x: byars_upper(x['Observed'], c), axis=1) / df['Expected'] * refvalue

    if metadata:
        method = np.where(df['Observed'] < 10, 'Exact', 'Byars')
        df = metadata_cols(df, f'indirectly standardized rate x {refvalue}', confidence, method)
    
    return df
