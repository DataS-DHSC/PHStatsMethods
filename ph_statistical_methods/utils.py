# -*- coding: utf-8 -*-

from scipy.special import ndtri
import pandas as pd
from scipy.stats import chi2

def get_calc_variables(a):
    """
    Creates the cumulative normal distribution and z score for a given alpha

    :param a: alpha
    :return: cumulative normal distribution, z score
    """
    norm_cum_dist = ndtri((100 + (100 - (100 * (1-a)))) / 200)
    z = ndtri(1 - (1-a )/ 2)
    return norm_cum_dist, z


def join_age_groups(df, col, age_df, age_col, group_cols = None):
    
    # Check number of rows
    if group_cols is not None:
        n_group_rows = df.groupby(group_cols).size().reset_index(name='counts')
    
        if n_group_rows.counts.nunique() > 1:
            raise ValueError('There must be the same number of rows per group')
            
        if n_group_rows.counts.unique() != len(age_df):
            raise ValueError('ref_df length must equal same number of rows in each group within data')
            
    else:
        if len(df) != len(age_df):
            raise ValueError('Dataframe, if ungrouped, must have same number of rows as reference data')

    # Get first number of age and sort ascending
    df['n1'] = df.apply(lambda x: str(re.findall(r'(\d+)', x[col])[0]), axis=1)
    age_df['n1'] = age_df.apply(lambda x: str(re.findall(r'(\d+)', x[age_col])[0]), axis=1)
    
    age_df = age_df.sort_values(by='n1').drop(age_col, axis=1)
    age_df['n1'] = age_df['n1'].rank()
    
    # order df values and assign over window
    df = df.sort_values(by='n1')
    if group_cols is not None:
        df['n1'] = df.groupby(group_cols)['n1'].rank()
    else:
        df['n1'] = df['n1'].rank()
    
    # join by columns
    df = df.merge(age_df, how='left', on='n1').drop('n1', axis=1)
    
    return df
    






