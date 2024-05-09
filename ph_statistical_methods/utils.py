# -*- coding: utf-8 -*-

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


import math
from scipy import stats 
import pandas as pd
import numpy as np


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
            obs_adjusted = obs
            z = stats.norm.ppf(0.5 + p / 2)
            test_statistic = obs_adjusted * (1 - 1 / (9 * obs_adjusted) - z / 3 / np.sqrt(obs_adjusted))**3
        elif side == "high":
            obs_adjusted = obs + 1
            z = stats.norm.ppf(0.5 + p / 2)
            test_statistic = obs_adjusted * (1 - 1 / (9 * obs_adjusted) + z / 3 / np.sqrt(obs_adjusted))**3

    test_statistic = test_statistic / expected
    return test_statistic


