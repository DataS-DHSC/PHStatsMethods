# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:49:06 2024

@author: Annabel.Westermann
"""

import pandas as pd
import numpy as np
import scipy.stats as scpy
import math as mt
from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data
from utils import exact_lowercl, exact_uppercl

def ph_rate(df, num_col, denom_col, group_cols = [], metadata = True, confidence = 0.95, multiplier = 100000):
    """
    Calculates rates uwith confidence limits using byars or exact method.

    :param df: dataframe containing the data to calculate rates for.
    :param num_col(str): name of the column containing the observed number of cases in the sample(numerator).
    :param denom_col(str): name of the column containing the number of cases in the sample(denominator).
    :param type: select which data you would like to return. "lower" is lower cl, "upper" is upper cl, "value" is value,
                 "standard" is value, lowercl, and uppercl, "full" is the default that will return all data.
    :param confidence: confidence level used for calculation, default is 0.95 for 95% confidence levels.
    :param multiplier: multiplier for calculation, defualt is 100000 for rates per 100000
    
    :returns: dataframe with calculated rates and confidence intervals.

    """
    
    #check and validate data
    confidence = validate_data(df,[num_col, denom_col], group_cols, confidence, metadata)
    
    if group_cols is not None:
        df = df.groupby(group_cols)[[num_col, denom_col]].apply(lambda x: x.sum(skipna=False)).reset_index()
        
    #calculate value column
    df["value"] = df[num_col] / df[denom_col] * multiplier
    
   #calculate confidence intervals
    if confidence is not None:
        for c in confidence:
            if num_col <10:
                df[ci_col[c, 'lower']] = df.apply(lambda y: exact_lowercl(y[num_col], y[denom_col], c))
                df[ci_col[c, 'upper']] = df.apply(lambda y: exact_uppercl(y[num_col], y[denom_col], c))
            else:
                df[ci_col[c, 'lower']] = df.apply(lambda y: byars_lower((y[num_col], c)/y[denom_col]*multiplier))
                df[ci_col[c, 'upper']] = df.apply(lambda y: byars_upper((y[num_col], c)/y[denom_col]*multiplier))
          
            #generate staistic and method columns
            if metadata:
               statistic = 'rate per 100000' if multiplier == 100000 else f'rate per {(multiplier)}'
               method = np.where(df[num_col] < 10, 'Exact', 'Byars')
               df = metadata_cols(df, statistic, confidence, method)
    
    return df 

