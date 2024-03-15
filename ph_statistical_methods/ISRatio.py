# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:58:18 2024

@author: Karandeep.Kaur
"""

import pandas as pd

from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data


def calculate_ISRatio(df, observations, population, ref, count_ref, pop_ref, group_cols = [],
                       confidence=0.95, refvalue=1, 
                      observed_totals=None,metadata=True):
    
    """
    Calculate Indirectly standardised ratios using calculate_ISRatio
    
    Calculates standard mortality ratios (or indirectly standardised ratios) with
    confidence limits using Byar's (1) or exact (2) CI method."""
    
    confidence = validate_data(df, [observations, population], group_cols, confidence, metadata)
    
    ref["Rates"]=ref[count_ref]/ref[pop_ref]

    population_info= len(df)//len(ref)
    
    repeat= pd.concat([ref]*population_info, ignore_index=True)
    
    full_df= pd.concat([df,repeat],axis=1)
    
    full_df["expected"]= full_df[population]*full_df["Rates"]
    
    if len(group_cols) > 0:
    
        grouped_df= full_df.groupby(group_cols)[[observations,"expected"]].sum().reset_index()
    
        grouped_df["Value"]=grouped_df[observations]/grouped_df["expected"]*refvalue
                                    
    if confidence is not None:
        
        for c in confidence:
            grouped_df[ci_col(c, 'lower')]= grouped_df.apply(lambda y: byars_lower(y[observations],(1-c))/y["expected"],axis=1)
            grouped_df[ci_col(c, 'upper')]= grouped_df.apply(lambda y: byars_upper(y[observations],(1-c))/y["expected"],axis=1)
            
    if metadata:
       statistic = f'indirectly standardised ratio x {refvalue}'
       grouped_df=metadata_cols(grouped_df, statistic, confidence, method = "Byars")
       
    return grouped_df
       
 


