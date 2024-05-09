# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:49:43 2024

@author: T.Vikneswaran_DHSC
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2
from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data, format_args, check_kwargs

def calculate_ISRate(df, num_col, denom_col, ref_num_col, ref_denom_col, group_cols, 
                     metadata=True, confidence=0.95, multiplier=100000, **kwargs):
    
    """Calculates indirectly standardized rates with confidence limits using Byar's or exact CI method.
    
    Args:
        df: DataFrame containing the data.
        num_col (str): Field containing observed number of events.
        denom_col (str): Field containing population at risk.
        ref_num_col (str): Observed events in the reference population.
        ref_denom_col (str): Population at risk in the reference population.
        group_cols: Columns to group data by.
        metadata (bool): Include metadata columns.
        confidence (float or list): Confidence levels, default 0.95.
        multiplier (int): The multiplier for the rate calculation, default 100000.
        
        **kwargs can include:
            ref_df: Reference DataFrame if separate.
            ref_join_cols: Join columns for ref_df.
            obs_df: Observed totals DataFrame if separate.
            obs_join_cols: Join columns for obs_df.
    """
    
    # Standardize and validate inputs
    confidence, group_cols = format_args(confidence, group_cols)
    ref_df, ref_join_left, ref_join_right = check_kwargs(df, kwargs, 'ref', ref_num_col, ref_denom_col)
    obs_df, obs_join_left, obs_join_right = check_kwargs(df, kwargs, 'obs', num_col)
    validate_data(df, denom_col, group_cols, metadata, ref_df=ref_df)

    # Merge reference data if provided
    if ref_df is not None:
        df = df.merge(ref_df, how='left', left_on=ref_join_left, right_on=ref_join_right).drop(ref_join_right, axis=1)
    
    # Calculate expected events
    df['Expected'] = df[ref_num_col].fillna(0) / df[ref_denom_col] * df[denom_col].fillna(0)

    # Calculate the reference rate
    df['ref_rate'] = df[ref_num_col].sum() / df[ref_denom_col].sum() * multiplier

    # Summarize data if observational totals are provided separately
    if obs_df is not None:
        df = df.groupby(group_cols)['Expected'].sum().reset_index()
        df = df.merge(obs_df, how='left', left_on=obs_join_left, right_on=obs_join_right)
    else:
        df = df.groupby(group_cols)[['Expected', num_col]].sum().reset_index()
    
    df = df.rename(columns={num_col: 'Observed'})
    
    # Calculate ISR
    df['Rate'] = df['Observed'] / df['Expected'] * df['ref_rate']
    
    # Calculate confidence intervals
    for c in confidence:
        df[ci_col(c, 'lower')] = df.apply(lambda x: byars_lower(x['Observed'], c), axis=1) / df['Expected'] * multiplier
        df[ci_col(c, 'upper')] = df.apply(lambda x: byars_upper(x['Observed'], c), axis=1) / df['Expected'] * multiplier

    # Append metadata if required
    if metadata:
        method = np.where(df['Observed'] < 10, 'Exact', 'Byars')
        df = metadata_cols(df, f'indirectly standardized rate per {multiplier}', confidence, method)
    
    return df

