# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from scipy import stats
from scipy.special import ndtri
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



def funnel_ratio_significance(obs, expected, p, side):
    """Calculate funnel ratio significance for given observations, expected value, probability, and side.

    Args:
        obs (int): Observations, an integer representing the number of observed events.
        
        expected (float): Expected value, a float representing the expected number of events under the null hypothesis.
        
        p (float): Probability, a float representing the probability threshold for significance.
        
        side (str): Side, a string that should be either 'high' or 'low', indicating the tail of the distribution to consider.

    Returns:
        float: Test statistic, a float representing the calculated test statistic for the funnel ratio significance.

    The function handles special cases for small sample sizes (less than 10) and a special condition when the observation is zero and considering the lower side. For larger sample sizes (10 or more), it uses adjusted formulas to compute the test statistic.
    """
    # Calculate z once
    z = stats.norm.ppf(0.5 + p / 2)
    
    # Calculate obs_adjusted based on the side
    obs_adjusted = obs if side == "low" else obs + 1
    
    # Check if obs_adjusted is zero to avoid division by zero error
    if obs_adjusted == 0:
        # Handle the division by zero error, set test_statistic to 0 or handle appropriately
        test_statistic = 0
    else:
        x = 1 - 1 / (9 * obs_adjusted) 
        y = (3 * np.sqrt(obs_adjusted))

        # Special case handling when observation is 0 and considering the lower side
        if obs == 0 and side == "low":
            test_statistic = 0
            
        # For small sample sizes (less than 10)
        elif obs < 10:
            if side == "low":
                degree_freedom = 2 * obs
                lower_tail_setting = False
            elif side == "high":
                degree_freedom = 2 * obs + 2
                lower_tail_setting = True
                
            # Chi-squared test statistic calculation
            if lower_tail_setting:
                test_statistic = stats.chi2.ppf(0.5 + p / 2, df=degree_freedom) / 2
            else:
                test_statistic = stats.chi2.ppf(1 - (0.5 + p / 2), df=degree_freedom) / 2

        # For larger sample sizes (10 or more)
        else:
            if side == "low":
                test_statistic = obs_adjusted * (x - z / y)**3
            elif side == "high":
                test_statistic = obs_adjusted * (x + z / y)**3

    test_statistic = test_statistic / expected
    
    return test_statistic



def euro_standard_pop():
    
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34',
                  '35-39', '40-44', '45-49', '50-54', '55-59', '60-64',
                  '65-69', '70-74', '75-79', '80-84', '85-89', '90+']
    
    pops = [5000, 5500, 5500, 5500, 6000, 6000, 6500, 7000, 7000, 7000, 
            7000, 6500, 6000, 5500, 5000, 4000, 2500, 1500, 1000]
    
    data = pd.DataFrame({'esp_age_bands': age_groups,
                         'euro_standard_pops': pops})
    
    return data


def join_euro_standard_pops(df, age_col, group_cols = None):
    
    if age_col not in df.columns:
        raise ValueError(f"'{age_col}' is not a column name in the data")
    
    # Check number of rows
    if group_cols is not None:
        n_group_rows = df.groupby(group_cols).size().reset_index(name='counts')
    
        if n_group_rows.counts.nunique() > 1:
            raise ValueError('There must be the same number of rows per group')
            
        if n_group_rows.counts.unique() != 19:
            raise ValueError('There must be 19 rows of data per group')
            
    else:
        if len(df) != 19:
            raise ValueError('Dataframe, if ungrouped, must have 19 rows for the 19 agebands')
    
    # Get euro standard pops and rank order
    esp = euro_standard_pop()
    esp['n1'] = list(range(1, 20))
    
    # Get first number of age and sort ascending
    df['n1'] = df.apply(lambda x: int(re.findall(r'(\d+)', str(x[age_col]))[0]), axis=1)
    
    if df['n1'].nunique() != 19:
        raise ValueError('There are duplicate minimum ages, which is not accepted as the function orders by the first number in each age band.\
                         For example, <5 and 5-10 IS NOT accepted but <=4 and 5-10 IS accepted.')
    
    # order df values and assign over window
    df = df.sort_values(by='n1')
    if group_cols is not None:
        df['n1'] = df.groupby(group_cols)['n1'].rank()
    else:
        df['n1'] = df['n1'].rank()
    
    # join by columns
    df = df.merge(esp, how='left', on='n1').drop('n1', axis=1)
    
    # Print out age bands for user to check
    print(df[[age_col, 'esp_age_bands']].drop_duplicates())
    print("Please check how the your ageband columns have joined to the 'esp_age_bands' above")
    
    return df


  
