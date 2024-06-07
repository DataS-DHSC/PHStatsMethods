# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from .confidence_intervals import student_t_dist
from .validation import metadata_cols, ci_col, validate_data, format_args

def ph_mean(df, num_col, group_cols, metadata = True, confidence = 0.95):
    
    """Calculates means with confidence limits using Student-t distribution.

    Parameters
    ----------
    df
        DataFrame containing the data to calculate proportions for.
    num_col : str
        Name of column containing observed number of cases in the sample
        (the numerator of the population).
    group_cols : str | list
        A string or list of column name(s) to group the data by. 
    metadata : bool
        Whether to include information on the statistic and confidence interval methods.
    confidence : float
        Confidence interval(s) to use, either as a float, list of float values or None.
        Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).

    Returns
    -------
    Pandas DataFrame
        DataFrame of calculated mean statistics with confidence intervals (df).
        
    Notes
    -----
    Student t-distribution is applied to calculate confidence intervals using the internal student_t() function.
    
    Examples
    --------
    Below is a example using the ph_mean() function to demonstrate the purpose of 
    package. 
      >>> import pandas as pd
      >>> from PHStatsMethods import *
      >>> df = pd.DataFrame({'area': ["Area1", "Area2", "Area3", "Area4"] * 3,
                             'numerator': [None, 48, 10000, 7, 82, 6500, 10000, 750, 9, 8200, 8, 900]})
      
      >>> ph_mean(df, 'numerator', 'area')
      >>> ph_mean(df, 'numerator', 'area', confidence = 0.998)
      >>> ph_mean(df, 'numerator', 'area', confidence = [0.95, 0.998])
      
    """
    
    # Check data and arguments
    confidence, group_cols = format_args(confidence, group_cols)
    df = validate_data(df, num_col, group_cols, metadata)
    
    if group_cols is None:
        raise TypeError('group_cols cannot be None for a mean statistic')

    # get grouped statistics
    df = df.groupby(group_cols)[num_col].agg([lambda x: x.sum(skipna=False), 
                                              lambda x: x.count(), 
                                              lambda x: x.std(skipna=False)]).reset_index()
    
    df = df.rename(columns={df.columns[-3]: 'value_sum', df.columns[-2]: 'value_count', df.columns[-1]: 'stdev'})
    
    df['Value'] = df['value_sum'] / df['value_count']
    
    for c in confidence:
        student_t = student_t_dist(df['value_count'], df['stdev'], c)
        df[ci_col(c, 'lower')] = df['Value'] - student_t
        df[ci_col(c, 'upper')] = df['Value'] + student_t

    if metadata:
        df = metadata_cols(df, 'Mean', confidence, "Student's t-distribution")
        
    if group_cols == ['ph_pkg_group']:
        df = df.drop(columns='ph_pkg_group') 
    
    return df