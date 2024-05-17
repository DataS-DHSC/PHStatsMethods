# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 11:38:17 2024

@author: Annabel.Westermann
"""

import pandas as pd
from pandas.api.types import is_numeric_dtype
from decimal import Decimal


def metadata_cols(df, statistic, confidence = None, method = None):
    """Applies columns to a dataframe detailing metadata used to produce that dataframe."
    
    Args:
        df: Pandas DataFrame.
        statistic (str): Statistic being produced
        confidence (float): Confidence(s) being calulated
        method (str): metjod used to calculate confidence intervals
        
    Returns:
        Pandas DataFrame detailing metadata used to calculate statistic (df)

    """
    
    df['Statistic'] = statistic
    
    if confidence is not None:
        df['Confidence'] = ', '.join([f'{int(c * 100)}%' if len(str(c)) < 5 else f'{c * 100}%' for c in confidence])
    
    if method is not None:
        df['Method'] = method
        
    return df
    

def ci_col(confidence_interval, ci_type = None):
    """Creates string relating to confidence interval calculated.
    
    Args:
        confidence_interval (float): confidence interval being calculated (e.g. 0.95, 0.998)
        ci_type (str): denotes upper or lower confidence interval status; default None
        
    Returns:
        col_name (str): a string for the column name containing the related confidence intervals calculated.
        
    """
    
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



###### VALIDATION CHECKS ######################################################


def check_cis(confidence):
    """Validates confidence intervals passed to a function. Ensures confidence interval is a float, within range (0.9 - 1), rounds to 4 d.p. where needed and ensures no duplicates. 

    Args:
        confidence (float | list): confidence interval(s) passed
        
    Returns:
        confidence (float | list): confidence interval(s) passed
        
    """
    
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
            
    return confidence



def format_args(confidence, group_cols = None):

    if confidence is not None: 
        if not isinstance(confidence, list):
            confidence = [confidence]
            
        confidence = check_cis(confidence)

    if group_cols is not None and not isinstance(group_cols, list):
        group_cols = [group_cols]

    if group_cols is None: 
        group_cols = ['ph_pkg_group']

    return confidence, group_cols



def check_arguments(df, columns, metadata = None):
    
    if not isinstance(df, pd.DataFrame):
        raise ValueError("'df' argument must be a Pandas DataFrame")
    
    # column names in dataframe and a string
    for col in columns:
        if not isinstance(col, str):
            # Writing 'quoted' as well to help R users of the package
            raise TypeError('Column names must be a quoted string')
        
        if col not in df.columns:
            raise ValueError(f"'{col}' is not a column header")
    
    #metadata is bool
    if metadata is not None and not isinstance(metadata, bool):
        raise TypeError("'metadata' must be either True or False")


## make sure nulls are np nan?
def validate_data(df, num_col, group_cols = None, metadata = None, denom_col = None, ref_df = None):
    
    # Allows us to group data when group_cols is None in format args.
    if group_cols == ['ph_pkg_group']:
        df['ph_pkg_group'] = 'ph_pkg_group'

    # adding this as not obvious to pass column as a list for developers using this function
    if group_cols is not None:
        if not isinstance(group_cols, list):
            raise TypeError("Pass 'group_cols' as a list")
            
        if ref_df is not None:
            n_group_rows = df.groupby(group_cols).size().reset_index(name='counts')
            
            if n_group_rows.counts.nunique() > 1:
                raise ValueError('There must be the same number of rows per group')
                
            if n_group_rows.counts.unique() != len(ref_df):
                raise ValueError('ref_df length must equal same number of rows in each group within data')
                
    numeric_cols = [num_col] if denom_col is None else [num_col, denom_col]

    check_arguments(df, (numeric_cols if group_cols is None else numeric_cols + group_cols), metadata)
            
    # check numeric columns
    for col in numeric_cols:
        if not is_numeric_dtype(df[col]):
            raise TypeError(f"'{col}' column must be a numeric data type")
        
        # No negative values
        if (df[col] < 0).any():
            raise ValueError('No negative numbers can be used to calculate these statistics')

    # Denominator must greater than 0
    if denom_col is not None:
        if (df[denom_col] <= 0).any():
            raise ValueError('Denominators must be greater than zero')

    return(df)



def check_kwargs(df, kwargs, ref_type, ref_num_col = None, ref_denom_col = None):
    
    if (ref_type + '_df') in kwargs.keys():
        ref_df = kwargs.get(ref_type + '_df')
        
        if (ref_type + '_join_left') not in kwargs.keys() or (ref_type + '_join_right') not in kwargs.keys():
            raise ValueError(f"'{ref_type}_df' given as a keyword argument but not '{ref_type}_join_left' and/or '{ref_type}_join_right'")
        
        else:
            join_left = kwargs.get(ref_type + '_join_left')
            join_right = kwargs.get(ref_type + '_join_right')
        
        join_left = [join_left] if isinstance(join_left, str) else join_left
        join_right = [join_right] if isinstance(join_right, str) else join_right
        
        validate_data(ref_df, num_col = ref_num_col, group_cols = join_right, denom_col = ref_denom_col)
        check_arguments(df, join_left)
        
        # remove columns in common to avoid duplicate columns after join
        same_cols = [col for col in df.columns if col in ref_df.columns and col not in join_left+join_right]
        if len(same_cols) > 0:
            ref_df = ref_df.drop(same_cols, axis=1)
        
        return (ref_df, join_left, join_right)
    
    else:
        validate_data(df, num_col = ref_num_col, denom_col = ref_denom_col)
       
        return(None, None, None)
    
    





                
     