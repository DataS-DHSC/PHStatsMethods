# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:58:18 2024

@author: Karandeep.Kaur
"""

import pandas as pd
import numpy as np

from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data, format_args, reference_pop_checks

                   
                           
        
def calculate_ISRatio(df, num_col, denom_col, ref_num_col, ref_denom_col, group_cols = [],
                       confidence=0.95, ref_df=None,refvalue=1, 
                       metadata=True, observed_totals=None):
    
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
        
        group_cols (list): A list of column name(s) to group the data by. Defaults to None.
        
        confidence (float): Confidence interval(s) to use, either as a float, list of float values or None.
        Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).
        
        refvalue (int): the standardised reference ratio, default = 1
        
        
        ref_df (Dataframe): If ref_num_col and ref_denom_col are not found within df a ref_df dataframe may be used
        ref_num_col and ref_denom_col will refer to the respective columns within ref_df. ref_df must also contain columns
        with the same naming conventions as found within df. e.g. if the reference data contains columns "sex" and "ageband"
        then these column names must be found in df.
        
        observed_totals (Dataframe): data.frame containing total observed events for each group, if not provided with 
        age-breakdowns in data. Must only contain the count field (num_col) plus grouping columns required to join to data using the
        same grouping column names; default = NULL
                 
    
    """
    
    
    confidence, group_cols = format_args(confidence, group_cols)
    
    if ref_df is not None:
    
        reference_pop_checks(df,group_cols=group_cols,ref_num_col=ref_num_col,
                                 ref_denom_col=ref_denom_col, ref_df=ref_df)       
                  
        join_cols = list(set(df.columns).intersection(ref_df.columns))

    
        df = df.merge(ref_df, how = 'left', on = join_cols)
    
    
    if observed_totals is None:
        
        validate_data(df, num_col, group_cols, metadata, denom_col)
        
    
        df = df.rename(columns= {num_col: "observed"})
        

        
        df['expected'] = df[ref_num_col].fillna(0) / df[ref_denom_col] * df[denom_col].fillna(0)
              
    
        df = df.groupby(group_cols)[["observed","expected"]].sum().reset_index()
    
    if observed_totals is not None:
    #else:
        validate_data(observed_totals, num_col, None, metadata)
            

            
        df['expected'] = df[ref_num_col].fillna(0) / df[ref_denom_col] * df[denom_col].fillna(0)
        
        df = df.groupby(group_cols)["expected"].sum().reset_index()
                
        obs_join_cols = list(set(df.columns).intersection(observed_totals.columns))
        
        
        df = df.merge(observed_totals, how = 'left', on = obs_join_cols)
        
        df = df.rename(columns= {num_col: "observed"})
        
        col_list = list(df.columns)
        
        x, y = col_list.index("expected"), col_list.index("observed")
        
        col_list[y], col_list[x] = col_list[x], col_list[y]
        
        df = df[col_list]
        
  
    df["Value"]=df["observed"]/df["expected"]*refvalue
                                    
        
    if confidence is not None: 

            for c in confidence:
                
                df[ci_col(c, 'lower')] = df.apply(lambda y: byars_lower(y["observed"],c)/y["expected"]* refvalue, axis=1)
                df[ci_col(c, 'upper')] = df.apply(lambda y: byars_upper(y["observed"],c)/y["expected"]* refvalue, axis=1)
        
    if metadata:
        method = np.where(df["observed"] < 10, 'Exact', 'Byars')
        df = metadata_cols(df, f'indirectly standardised ratio x {refvalue}', confidence, method)


    return df



