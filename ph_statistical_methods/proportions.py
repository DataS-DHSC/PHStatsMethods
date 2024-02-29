# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 16:52:40 2024

@author: Annabel.Westermann
"""

import pandas as pd

from ph_statistical_methods.confidence_intervals import wilson, wilson_lower, wilson_upper
from ph_statistical_methods.validation import metadata_cols, ci_col

#df = pd.read_excel('ph_statistical_methods/unit_tests/test_data/testdata_Proportion.xlsx')

df = pd.DataFrame({'area': ['Area1', 'Area2', 'Area3','Area4']*3,
                  'num': [None, 82, 9, 48, 65, 8200, 10000, 10000, 8, 7, 750, 900],
                  'den': [100, 10000, 10000, 10000] * 3})



def ph_proportion_calc(numerator, denominator, multiplier = 1, confidence = None):
    
    proportion = (numerator / denominator) * multiplier
    
    if confidence is not None:
        prop_dict = {}
        prop_dict['Proportion'] = proportion
        
        # handle parameter if passed as float
        # TODO: make this part of the formatting checks! 
        if isinstance(confidence, float):
            confidence = [confidence]
        
        # get confidence interval for all given confidence intervals
        for c in confidence:
            prop_dict[ci_col(c)] = wilson(numerator, denominator, c)
        
        # set return object to dictionary
        proportion = prop_dict
        
    return proportion


        
def ph_proportion(df, num_col, denom_col, metadata = True, confidence = 0.95, multiplier = 1):
    
    df['Value'] = df.apply(lambda y: ph_proportion_calc(y[num_col], y[denom_col], multiplier),
                           axis=1)

    if confidence is not None:
        if isinstance(confidence, float):
            confidence = [confidence]
    
        for c in confidence:
            df[f'lower_{ci_col(c)}'] = df.apply(lambda y: wilson_lower(y[num_col], y[denom_col], c),
                                                axis=1)
            df[f'upper_{ci_col(c)}'] = df.apply(lambda y: wilson_upper(y[num_col], y[denom_col], c),
                                                axis=1)
            
    if metadata:
        statistic = 'Percentage' if multiplier == 100 else f'Proportion of {multiplier}'
        df = metadata_cols(df, statistic, confidence, 'Wilson')
        
    return df
    

