# -*- coding: utf-8 -*-

from scipy.special import ndtri
import math
from scipy import stats 
import pandas as pd
import numpy as np

def get_calc_variables(a):
    """
    Creates the cumulative normal distribution and z score for a given alpha

    :param a: alpha
    :return: cumulative normal distribution, z score
    """
    norm_cum_dist = ndtri((100 + (100 - (100 * (1-a)))) / 200)
    z = ndtri(1 - (1-a )/ 2)
    return norm_cum_dist, z


def poisson_cis(z, x_a, x_b):
    
    q =1
    tot = 0
    s = 0
    k= 0
    
    while k<= z or q > tot * 1e-10:
        tot += q
        if x_a <= k <= x_b:
            s+= q
        if tot > 1e30:
            s /= 1e30
            tot /= 1e30
            q /= 1e30
        
        k += 1
        q*= z / k
    
    return s / tot


def poisson_funnel(obs, p, side):
    """
    Calculates the poisson distrbution, takes in observations, poisson standard deviation, and side.
    :param obs: Observations as integer
    :param p: Poisson stamdard deviation, given as float, 2 sigma is 0.025, 3 sigma is 0.001
    :param side: Side given as str, value can be "high" or "low"
    :return p_funnel: Poisson funnel given as float

    """
    v = 0.5
    dv = 0.5

    if side == "low":

    # this is in the Excel macro code, but obs can't be 0 based on Funnels.R
    # if (obs == 0) return(0)

     while dv > 1e-7 :
      dv = dv / 2

      if (poisson_cis((1 + obs) * v / (1 - v),
                      obs,
                      10000000000) > p) :
        v = v - dv
      
      else:
        v = v + dv
     

    elif side == "high":

     while dv > 1e-7: 
      dv = dv / 2
      if (poisson_cis((1 + obs) * v / (1 - v),
                      0,
                      obs) < p):
        v = v - dv
      else:
        v = v + dv

    p_funnel = (1 + obs) * v / (1 - v)
    return p_funnel



def funnel_ratio_significance(obs, expected, p, side):
    """
    Calculate funnel ratio significance for given observations, expected value, probability, and side.
    :param obs: Observations, integer.
    :param expected: Expected value, float.
    :param p: Probability, float.
    :param side: Side, 'high' or 'low'.
    :return: Test statistic, float.
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


