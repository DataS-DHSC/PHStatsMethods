# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:52:40 2024

@author: Hadley.Nanayakkara
"""

import pandas as pd

from .validation import format_args, check_arguments

def ph_quantile(df, values, group_cols = None, nquantiles = 10, invert = True, type = "full"):
    """Assigns data to quantiles based on numeric data rankings.

    Args:
        df: a data frame containing the quantitative data to be assigned to quantiles. 
            If group_cols is used, separate sets of quantiles will be assigned for each grouping set
        values (str): field name from data containing the numeric values to rank data by and assign quantiles.
        group_cols: A string or list of column name(s) to group the data by. 
                Defaults to None.
        nquantiles (int): the number of quantiles to separate each grouping set into.
        invert (bool) or (str): whether the quantiles should be directly (False) or inversely (True) related
                    to the numerical value order OR unquoted string referencing field name from data that 
                    stores logical values for each grouping set.
        type (str): defines whether to include metadata columns in output to reference the arguments 
                    passed; can be "standard" or "full".

    Returns:
        When type = "full", returns the original data.frame with quantile 
        (quantile value), nquantiles (number of quantiles requested), groupvars 
        (grouping sets quantiles assigned within) and invert (indicating direction 
        of quantile assignment) fields appended.
        
    """

    # Check data and arguments
    cols = values
    null, group_cols = format_args(None, group_cols)

    if group_cols is not None:
        if not isinstance(group_cols, list):
            raise TypeError("Pass group_cols as a list")
    
    if not isinstance(values, str):
        raise TypeError("Pass 'values' as a string")
    
    if not isinstance(nquantiles, int):
        raise TypeError("Pass 'nquantiles' as a integer")
    
    if not isinstance(invert, (bool, str))):
        raise TypeError("Pass 'invert' as either a boolean or a string")
    
    if isinstance(invert, str): cols += invert
    check_arguments(df, cols if group_cols is None else cols + group_cols)