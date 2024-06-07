# -*- coding: utf-8 -*-

import pandas as pd

from .confidence_intervals import wilson_lower, wilson_upper
from .validation import metadata_cols, ci_col, format_args, validate_data, group_args


def ph_proportion(df, num_col, denom_col, group_cols = None, metadata = True, confidence = 0.95, multiplier = 1):
    """Calculates proportions with confidence limits using Wilson Score method.

    Parameters
    ----------
    df
        DataFrame containing the data to calculate proportions for.
    num_col : str
        Name of column containing observed number of cases in the sample
        (the numerator of the population).
    denom_col : str
        Name of column containing number of cases in sample 
        (the denominator of the population).
    group_cols : str | list
        A string or list of column name(s) to group the data by. 
        Defaults to None.
    metadata : bool
        Whether to include information on the statistic and confidence interval methods.
    confidence : float 
        Confidence interval(s) to use, either as a float, list of float values or None.
        Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).
    multiplier : int
        Multiplier used to express the final values (e.g. 100 = percentage).

    Returns
    -------
    Pandas DataFrame
        DataFrame of calculated proportion statistics with confidence intervals.
    
    Notes
    -----
    Wilson Score method (2) is applied using the internal wilson_lower and wilson_upper functions.

    References
    ----------
    (1) Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg 209 to 212.
    (2) Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.

    Examples
    --------
    Below is a example using the ph_proportion() function to demonstrate the purpose of 
    package. 
      >>> import pandas as pd
      >>> from PHStatsMethods import *
      >>> df = pd.DataFrame({'area': ["Area1", "Area2", "Area3", "Area4"] * 3,
                             'numerator': [None, 48, 10000, 7, 82, 6500, 10000, 750, 9, 8200, 8, 900],
                             'denominator': [100, 10000, 10000, 10000] * 3})

    Ungrouped 

      >>> ph_proportion(df, 'numerator', 'denominator')
      >>> ph_proportion(df, 'numerator', 'denominator', confidence = 0.998)
      >>> ph_proportion(df, 'numerator', 'denominator', confidence = [0.95, 0.998])

    Grouped

      >>> ph_proportion(df, 'numerator', 'denominator', 'area', multiplier = 100)
      
    """

    # Check data and arguments
    confidence, group_cols = format_args(confidence, group_cols)
    df = validate_data(df, num_col, group_cols, metadata, denom_col)
        
    if not isinstance(multiplier, int) or multiplier <= 0:
        raise ValueError("'Multiplier' must be a positive integer")
      
    if (df[num_col] > df[denom_col]).any():
        raise ValueError('Numerators must be less than or equal to the denominator for a proportion statistic')   
    
    # Grouping by temporary column to reduce duplication in code
    df, group_cols = group_args(df, group_cols, False)

    # Sum Numerator and Denominator columns, ensure NAs are included. 
    df = df.groupby(group_cols)[[num_col, denom_col]].apply(lambda x: x.sum(skipna=False)).reset_index()

    ### Calculate statistic
    df['Value'] = (df[num_col] / df[denom_col]) * multiplier

    if confidence is not None:
        for c in confidence:
            df[ci_col(c, 'lower')] = df.apply(lambda y: wilson_lower(y[num_col], y[denom_col], c),
                                                axis=1) * multiplier
            df[ci_col(c, 'upper')] = df.apply(lambda y: wilson_upper(y[num_col], y[denom_col], c),
                                                axis=1) * multiplier
            
    if metadata:
        statistic = 'Percentage' if multiplier == 100 else f'Proportion of {multiplier}'
        df = metadata_cols(df, statistic, confidence, 'Wilson')
        
    if group_cols == ['ph_pkg_group']:
        df = df.drop(columns='ph_pkg_group') 
        
    return df
