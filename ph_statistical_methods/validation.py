# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 11:38:17 2024

@author: Annabel.Westermann
"""

import pandas as pd


def metadata_cols(df, statistic, confidence = None, method = None):
    
    df['Statistic'] = statistic
    
    if confidence is not None:
        df['Confidence'] = ', '.join([str(n) for n in confidence])
        df['Method'] = method
        
    return df
    

def ci_col(confidence_interval):
    
    percent = str(confidence_interval)[2:].ljust(2, '0')
    
    # use underscore to represent decimal place
    if len(percent) > 2:
        percent = percent[:2] + '_' + percent[2:]
    
    return percent + '_ci'
    


###### VALIDATION CHECKS
    
## round to 2 decimal places (CI) and check they're not the same




