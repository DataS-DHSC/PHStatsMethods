# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:49:06 2024

@author: Annabel.Westermann
"""

import pandas as pd
import scipy.stats as scpy
import math as mt
from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data

def phe_rate(df, num_col, denom_col, type = "full", confidence = 0.95, multiplier = 100000):
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
    
    confidence = validate_data(df, num_col, denom_col, confidence)
    
    if type != "value" | "upper" | "lower" | "standard" | "full":
        print("type must be either value, upper, lower, standard or full")
        
    df["value"] = df[num_col] / df[denom_col] * multiplier
    
    if confidence is not None:
        for c in confidence:
            if num_col <10:
                df[ci_col[c, 'lower']] = scpy.chi2(1-confidence)/2, 2*num_col/2/denom_col * multiplier
            else:
                df[ci_col[c, 'lower']] = byars_lower((num_col, confidence)/denom_col * multiplier )
            if
            