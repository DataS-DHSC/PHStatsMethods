# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 17:34:08 2024

@author: Annabel.Westermann
"""
import scipy.stats as st
from math import floor, ceil, sqrt

def poisson_cis(z, x_a, x_b):
    """Calculates the cumulative dribution function of a Poisson distribution.
    
    Args:
        z (int | float): The average rate of occurence of events within a fixed interval of time or space.
        x_a (int | float): The lower bound of the interval to be used in the calculation.
        x_b (int | float): The upper bound of the interval to be used in the calculation.
    Returns:
        (float) The cumulative probability of a number of events falling between the intervals given the average rate.
    
    """
    
    q = 1
    tot = 0
    s = 0
    k = 0
    
    #if any(val < 0 for val in [z, x_a, x_b] or
    #x_b < x_a or
    #x_a % 1 > 0 or
    #x_b % 1 > 0):
        #return None
        
    while k <= z or q > tot * 1e-10:
        tot += q
        if x_a <= k <= x_b:
            s += q
        if tot > 1e30:
            s /= 1e30
            tot /= 1e30
            q /= 1e30
            
        k += 1
        q *= z / k
        
    return s / tot


def poisson_funnel(obs, p, side):
    """Calculates the poisson distrbution, takes in observations, poisson standard deviation, and side.
    
    Args:
        obs (int): Observations as integer
        p (float): Poisson stamdard deviation, given as float, 2 sigma is 0.025, 3 sigma is 0.001
        side (str): Side given as str, value can be "high" or "low"
    Returns:
        p_funnel (float): Poisson funnel

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
    z = st.norm.ppf(0.5 + p / 2)
    
    # Calculate obs_adjusted based on the side
    obs_adjusted = obs if side == "low" else obs + 1
    
    # Check if obs_adjusted is zero to avoid division by zero error
    if obs_adjusted == 0:
        # Handle the division by zero error, set test_statistic to 0 or handle appropriately
        test_statistic = 0
    else:
        x = 1 - 1 / (9 * obs_adjusted) 
        y = (3 * sqrt(obs_adjusted))

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
                test_statistic = st.chi2.ppf(0.5 + p / 2, df=degree_freedom) / 2
            else:
                test_statistic = st.chi2.ppf(1 - (0.5 + p / 2), df=degree_freedom) / 2

        # For larger sample sizes (10 or more)
        else:
            if side == "low":
                test_statistic = obs_adjusted * (x - z / y)**3
            elif side == "high":
                test_statistic = obs_adjusted * (x + z / y)**3

    test_statistic = test_statistic / expected
    return test_statistic



def sigma_adjustment(p, population, average_proportion, side, multiplier):
    """
    Calculate the proportion funnel point value for a specific population based on a population average value
    
    Args:
        p (int | float: Probability to calculate funnel plot point (noramlly 0.975 or 0.999)
        must be a numeric value between 0 and 1.
        population (int): Population for the area
        average_proportion (int | float) : The average proportion for all the areas in the funnel plot
        side (str): determines which funnel to calculate, possible values are "low" and "high"
        multiplier (int): multiplier used to express final values - default = 100 (100 = percentage)

    Returns:
        A value equivalent to the specified funnel point plot.
        
    """
    
    first_part = average_proportion * (population / st.norm.ppf(p)**2 + 1)
    
    adj = sqrt((-8 * average_proportion * (population / st.norm.ppf(p)**2 + 1))**2 - 64 *
                    (1 / st.norm.ppf(p)**2 + 1 / population) * average_proportion  *
                    (population * (average_proportion * (population / st.norm.ppf(p)**2 + 2) -1)
                    + st.norm.ppf(p)**2 * (average_proportion -1)))
    
    last_part = (1 / st.norm.ppf(p)**2 + 1 / population)
    
    if side == "low":
        adj_return = (first_part - adj / 8) / last_part
    elif side == "high":
        adj_return = (first_part + adj / 8) / last_part
    
    adj_return = (adj_return / population) * multiplier
    
    return(adj_return)


def signif_floor(x, percentage_down=0.95):
    n = len(str(floor(x * percentage_down))) - 1
    y = floor(x * percentage_down / 10**n) * 10**n
    y = 0 if x == 0 else y
    return y


def signif_ceiling(x, percentage_up=1.05):
    n = len(str(ceil(x * percentage_up))) - 2
    y = ceil(x * percentage_up / 10**n) * 10**n
    y = 0 if x == 0 else y
    return y






