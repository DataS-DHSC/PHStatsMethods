# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import warnings

from .validation import format_args, check_arguments, group_args

def ph_quantile(df, values, group_cols = None, nquantiles = 10, invert = True, type = "full"):
    """Assigns data to quantiles based on numeric data rankings.

    Parameters
    ----------
    df
        A data frame containing the quantitative data to be assigned to quantiles. 
        If group_cols is used, separate sets of quantiles will be assigned for each grouping set
    values : str  
        Column name from data containing the numeric values to rank data by and assign quantiles.
    group_cols: str | list
        A string or list of column name(s) to group the data by. 
        Defaults to None.
    nquantiles : int
        The number of quantiles to separate each grouping set into.
    invert : bool
        Whether the quantiles should be directly (False) or inversely (True) related
        to the numerical value order.
    type : str 
        Defines whether to include metadata columns in output to reference the arguments 
        passed; can be "standard" or "full".

    Returns
    -------
    Pandas DataFrame
        When type = "full", returns the original data.frame with quantile 
        (quantile value), nquantiles (number of quantiles requested), groupvars 
        (grouping sets quantiles assigned within) and invert (indicating direction 
        of quantile assignment) fields appended.

    Notes
    -----
    See `OHID Technical Guide - Assigning Deprivation Categories 
    <https://fingertips.phe.org.uk/documents/OHID%20Guidance%20-%20Assigning%20Deprivation%20Categories.pdf>`_ 
    for methodology. In particular, note that this function strictly applies the algorithm defined but
    some manual review, and potentially adjustment, is advised in some cases where multiple small
    areas with equal rank fall across a natural quantile boundary.
    
    Example
    -------
    
    Below is an example use of the ph_quantile() function to demonstrate 
    the purpose of the package.
    
    >>> import pandas as pd
    >>> from PHStatsMethods import *
    >>> df = pd.DataFrame({'area': ["Area1", "Area2", "Area3", "Area4"] * 3,
                           'numerator': [None, 48, 10000, 7, 82, 6500, 10000, 750, 9, 8200, 8, 900]})
    
    Ungrouped
    
    >>> ph_quantile(df, 'numerator')
    >>> ph_quantile(df, 'numerator', nquantiles = 4)
    >>> ph_quantile(df, 'numerator', invert = False)
    >>> ph_quantile(df, 'numerator', type = "standard")
    
    >>> ph_quantile(df, 'numerator', group_cols = 'area')
    >>> ph_quantile(df, 'numerator', group_cols = 'area', nquantiles = 4, type = "standard")
        
    """
    # Ensure original df remains unchanged 
    df = df.copy()

    # Check data and arguments
    null, group_cols = format_args(None, group_cols)

    if group_cols is not None:
        if not isinstance(group_cols, list):
            raise TypeError("Pass group_cols as a list")
    
    if not isinstance(values, str):
        raise TypeError("Pass 'values' as a string")
    
    if not isinstance(nquantiles, int):
        raise TypeError("Pass 'nquantiles' as a integer")
    
    if not isinstance(invert, bool):
        raise TypeError("Pass 'invert' as a boolean")

    # Grouping by temporary column to reduce duplication in code
    df, group_cols = group_args(df, group_cols, True)
    
    check_arguments(df, [values] if group_cols is None else [values] + group_cols)
    
    # Additional columns in output
    df['nquantiles'] = nquantiles

    # Calculate Quantiles  
    df['num_rows'] = df.groupby(group_cols)[values].transform(lambda x: x.count()) # Number of rows in each group
    df['rank'] = df.groupby(group_cols)[values].rank(ascending = not invert, method='min') # Rank each value in each group


    # Assign a quantile based on rank and number of rows in each group 
    df['quantile'] = np.where(df['num_rows'] < nquantiles,
                              np.nan,
                              np.floor((nquantiles + 1) - np.ceil(((df['num_rows'] + 1) - df['rank']) / (df['num_rows'] / nquantiles))))

    # The above maths means that rank 1 may occasionally become quantile 0, instead of quantile 1
    df.loc[df['quantile'] == 0, 'quantile'] = 1

    if invert is True:
        df['qinverted'] = "lowest quantile represents highest values"
    else:
        df['qinverted'] = "lowest quantile represents lowest values"

    # Generate warnings 
    if df['quantile'].isna().any():
        warnings.warn("One or more groups had too few small areas with values to allow quantiles to be assigned",
                      UserWarning)

    # Drop columns if required
    if type == "standard":
        df = df.drop(['num_rows', 'rank', 'nquantiles', 'qinverted'], axis=1)
        
    if group_cols == ['ph_pkg_group']:
        df = df.drop(columns='ph_pkg_group')

    return df
