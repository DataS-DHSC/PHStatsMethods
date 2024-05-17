# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:58:18 2024

@author: Karandeep.Kaur
"""

import pandas as pd
import numpy as np

from .confidence_intervals import byars_lower, byars_upper
from .validation import metadata_cols, ci_col, validate_data, format_args, check_kwargs


def ph_ISRatio(df, num_col, denom_col, ref_num_col, ref_denom_col, group_cols = None, 
                      metadata = True, confidence = 0.95, refvalue = 1, **kwargs):
    
    """Calculates standard mortality ratios (or indirectly standardised ratios) with
    confidence limits using Byar's (1) or exact (2) CI method.
    
    Args:
        df: DataFrame containing the data to calculate IS ratios for.
        
        num_col (str): field name from data containing the observed number of events for
        each standardisation category (e.g. ageband) within each grouping set (eg area). If observed_totals is not None,
        then num_col will contain the observations from the observed_totals dataframe.
        
        denom_col (str): field name from data containing the population for each standardisation 
        category (e.g. age band).
        
        ref_num_col (str): the observed number of events in the reference population for
        each standardisation category (eg age band); field name from df or ref_def.
        
        ref_denom_col (str): the reference population for each standardisation category (eg age band)
        
        group_cols: A string or list of column name(s) to group the data by.
        
        confidence (float): Confidence interval(s) to use, either as a float, list of float values or None.
        Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).

        refvalue (int): the standardised reference ratio, default = 1
        
    **kwargs:
        ref_df
        ref_join_left
        ref_join_right
        obs_df
        obs_join_left
        obs_join_right
        
    Returns:
        df: Dataframe containing calculated IS Ratios.

    """

    # validate data - TODO: check group by row lengths?
    confidence, group_cols = format_args(confidence, group_cols)
    ref_df, ref_join_left, ref_join_right = check_kwargs(df, kwargs, 'ref', ref_num_col, ref_denom_col)
    obs_df, obs_join_left, obs_join_right = check_kwargs(df, kwargs, 'obs', num_col)
    df = validate_data(df, denom_col, group_cols, metadata, ref_df = ref_df)
    
    if ref_df is not None:
        df = df.merge(ref_df, how = 'left', left_on = ref_join_left, right_on = ref_join_right).drop(ref_join_right, axis=1)
    
    df['exp_x'] = df[ref_num_col].fillna(0) / df[ref_denom_col] * df[denom_col].fillna(0)
    
    ## TODO: must be a groupby?
    if obs_df is not None:
        df = df.groupby(group_cols)[['exp_x']].apply(lambda x: x.sum(skipna=False)).reset_index()
        df = df.merge(obs_df, how = 'left', left_on = obs_join_left, right_on = obs_join_right)
    else:
        df = df.groupby(group_cols)[['exp_x', num_col]].sum().reset_index()
        
    df = df.rename(columns={num_col: 'Observed', 'exp_x': 'Expected'}).reindex(columns=(group_cols + ['Observed', 'Expected']))
    
    df['Value'] = df['Observed'] / df['Expected'] * refvalue
    
    for c in confidence:
        df[ci_col(c, 'lower')] = df.apply(lambda x: byars_lower(x['Observed'], c), axis=1) / df['Expected'] * refvalue
        df[ci_col(c, 'upper')] = df.apply(lambda x: byars_upper(x['Observed'], c), axis=1) / df['Expected'] * refvalue

    if metadata:
        method = np.where(df['Observed'] < 10, 'Exact', 'Byars')
        df = metadata_cols(df, f'indirectly standardised ratio x {refvalue}', confidence, method)
        
    if group_cols == ['ph_pkg_group']:
        df = df.drop(columns='ph_pkg_group') 
    
    return df
    
    
    