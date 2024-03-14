# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 11:38:17 2024

@author: Annabel.Westermann
"""

import pandas as pd
from pandas.api.types import is_numeric_dtype
from decimal import Decimal


def metadata_cols(df, statistic, confidence = None, method = None):
    
    df['Statistic'] = statistic
    
    if confidence is not None:
        df['Confidence'] = ', '.join([str(n) for n in confidence])
        df['Method'] = method
        
    return df
    

def ci_col(confidence_interval, ci_type = None):
    
    if ci_type not in ['upper', 'lower', None]:
        raise ValueError("'ci_type' must be either 'upper', 'lower' or None")
    
    percent = str(confidence_interval)[2:].ljust(2, '0')
    
    # use underscore to represent decimal place
    if len(percent) > 2:
        percent = percent[:2] + '_' + percent[2:]
        
    col_name = percent + '_ci'
    
    if ci_type is not None:
        col_name = f'{ci_type}_{col_name}'
    
    return col_name
    
    
def convert_args_to_list(confidence, group_cols = None):

    if not isinstance(confidence, list):
        confidence = [confidence]

    if group_cols is None:
        group_cols = []

    if not isinstance(group_cols, list):
        group_cols = [group_cols]

    return confidence, group_cols


###### VALIDATION CHECKS ######################################################


def check_cis(confidence):
        
    for c in confidence:
        if not isinstance(c, float):
            raise TypeError('Confidence intervals must be of type: float')
            
        if c < 0.9 or c >= 1:
            raise ValueError('Confidence intervals must be between 0.9 and 1')
    
    # Use Decimal module to round .5 properly and round to 4dp
    confidence = [float(round(Decimal(str(c)), 4)) for c in confidence]
        
    same_ci = list(set([x for x in confidence if confidence.count(x) > 1]))
    
    if len(same_ci) > 0:
        raise ValueError('There are duplicate confidence intervals (when rounded to 4dp): '\
                         + ', '.join([str(n) for n in same_ci])) 



def check_arguments(df, columns, metadata = None):
    
    if not isinstance(df, pd.DataFrame):
        raise ValueError("'df' argument must be a Pandas DataFrame")
    
    # column names in dataframe and a string
    for col in columns:
        if not isinstance(col, str):
            # Writing 'quoted' as well to help R users of the package
            raise TypeError('Column names must be a quoted string')
        
        if col not in df.columns:
            raise ValueError(f'{col} is not a column header')
    
    #metadata is bool
    if metadata is not None and not isinstance(metadata, bool):
        raise TypeError("'Metadata' must be either True or False")



def validate_data(df, num_col, group_cols, confidence, metadata, denom_col = None):
    
    # adding this as not obvious to pass column as a list for developers using this function
    if not isinstance(group_cols, list):
        raise TypeError('Pass group_cols as a list')
    
    numeric_cols = [num_col] if denom_col is None else [num_col, denom_col]
    
    check_arguments(df, numeric_cols + group_cols, metadata)
    
    confidence = check_cis(confidence)
            
    # check numeric columns
    for col in numeric_cols:
        if not is_numeric_dtype(df[col]):
            raise TypeError(f'{col} column must be a numeric data type')
        
        # No negative values
        if (df[col] < 0).any():
            raise ValueError('No negative numbers can be used to calculate these statistics')

    # Denominator must greater than 0
    if denom_col is not None:
        if (df[denom_col] <= 0).any():
            raise ValueError('Denominators must be greater than zero')

        if (df[num_col] > df[denom_col]).any():
            raise ValueError('Numerators must be less than or equal to the denominator for a proportion statistic')
 
