# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:19:00 2024

@author: Annabel.Westermann
"""

import numpy as np
import warnings
from math import sqrt
from scipy.stats import chi2, norm
from scipy import stats

from .utils import get_calc_variables

def wilson_lower(count, denominator, confidence=0.95):

    """Calculates the lower CI using Wilson Score method [1, 2]. Takes in value, numerator, denominator, and confidence
     (default 0.95)
    [1] Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg
    209 to 212.
    [2] Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence
     (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.
     
    Args:
        count (int | float): Numerator
        denominator (int | float): Denominator
        confidence (float): confidence - default 0.95 for 95% confidence interval
    Returns: 
        Lower confidence interval (float)
        
    """
    norm_cum_dist, z = get_calc_variables(confidence)
    lower_ci = ((2 * count + norm_cum_dist ** 2 - norm_cum_dist * sqrt(norm_cum_dist ** 2 + 4 * count * (1 -
                (count / denominator )))) / 2 / (denominator + norm_cum_dist ** 2))
    return lower_ci


def wilson_upper(count, denominator, confidence=0.95):

    """Calculates the upper CI using Wilson Score method [1, 2]. Takes in value, numerator, denominator, and confidence
     (default 0.95)
    [1] Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg
    209 to 212.
    [2] Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence
     (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.
     
    Args:
        count (int | float): Numerator
        denominator (int | float): Denominator
        confidence (float): confidence - default 0.95 for 95% confidence interval
    Returns: 
        Upper confidence interval (float)
        
    """
    norm_cum_dist, z = get_calc_variables(confidence)
    upper_ci = (2 * count + norm_cum_dist ** 2 + norm_cum_dist * sqrt(norm_cum_dist ** 2 + 4 * count * (1 - (count /
                denominator )))) / 2 / (denominator + norm_cum_dist ** 2) 
    return upper_ci


def wilson(count, denominator, confidence=0.95):

    """Calculates the CI using Wilson Score method [1, 2]. Takes in value, numerator, denominator, and confidence
     (default 0.95)
    [1] Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg
    209 to 212.
    [2] Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence
     (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.
     
    Args:
        count (int | float): Numerator
        denominator (int | float): Denominator
        confidence (float): confidence - default 0.95 for 95% confidence interval
    Returns:
        Lower and Upper confidence intervals(tuple)
        
    """
    return wilson_lower(count, denominator, confidence), wilson_upper(count, denominator, confidence)


def exact_upper(value, confidence=0.95):
    
    """Calculates upper confidence interval using the exact method[1].
    [1] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    Args:
        value (int | float): Value to calculate upper confidence interval
        confidence (float): Confidence - default 0.95 for 95% confidence interval
    Returns:
        Upper confidence interval (float)
        
    """
    o = 2 * value + 2
    upper_ci = chi2.ppf(1 - ((1 - confidence) / 2), o) / 2
    return upper_ci


def exact_lower(value, confidence=0.95):
    
    """Calculates lower confidence interval using the exact method[1].
    [1] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    Args:
        value (int | float): Value to calculate lower confidence interval
        confidence (float): Confidence - default 0.95 for 95% confidence interval
    Returns:
        Lower confidence interval (float)
        
    """
    o = 2 * value
    lower_ci = chi2.ppf((1 - confidence) / 2, o) / 2
    return lower_ci


def exact(value, confidence=0.95):

    """Calculates confidence intervals using the exact method[1].
    [1] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    Args:
        value (int | float): Value to calculate confidence intervals
        confidence (float): Confidence - default 0.95 for 95% confidence interval
    Returns: 
        Lower and Upper confidence intervals (tuple)
        
    """
    return exact_lower(value, confidence=confidence), exact_upper(value, confidence=confidence)



def byars_lower(value, confidence=0.95):
    
    """Calculates lower confidence interval using Byar's method[1].
    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.

    Args:
        value (int | float): Value to calculate lower confidence interval
        confidence (float): Confidence - default 0.95 for 95% confidence interval
    Returns: 
        Lower confidence interval (float)
        
    """
    if value < 0:
        raise ValueError("'Value' must be a positive number")
    
    z = norm.ppf(confidence + (1-confidence)/2)
    
    if value < 10:
        return exact_lower(value, confidence)
    else:
        return value * (1 - 1 / (9 * value) - z / (3 * sqrt(value))) ** 3


# calculates the upper CI using Byar's method without using denominator. Takes in count and alpha (default 0.05)
def byars_upper(value, confidence=0.95):
    """Calculates upper confidence interval using Byar's method[1].
    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.

    Args:
        value (int | float): Value to calculate upper confidence interval
        confidence (float): Confidence - default 0.95 for 95% confidence interval
    Returns: 
        Upper confidence interval (float)
        
    """
    if value <= 0:
        raise ValueError("'Value' must be a positive number")
        
    z = norm.ppf(confidence + (1-confidence)/2)
    
    if value < 10:
        return exact_upper(value, confidence)
    else:
        return (value + 1) * (1 - 1 / (9 * (value + 1)) + z / (3 * sqrt(value + 1))) ** 3


# calculates the upper and lower CIs using Byar's method without denominator and returns in a tuple
def byars(value, confidence=0.95, denominator=None, rate=None, exact_method_for_low_numbers=True):
    
    """Calculates confidence intervals using Byar's method[1].
    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.

    Args:
        value (int | float): Value to calculate confidence intervals, must be over 9 to calculate Byar's, else exact method is used
        confidence (float): Confidence - default 0.95 for 95% confidence interval
        denominator (int | float): (Optional) Denominator to calculate Byar's on a rate
        rate (int | float): (Optional) Rate
        exact_method_for_low_numbers (bool): Boolean instruction as to whether to use exact method for low numbers. Default
                                         True
    Returns: Either exact method or Byar's method confidence intervals in a tuple
    
    """
    if denominator and not rate or rate and not denominator:
        raise ValueError('To use a denominator, you must also provide a rate')
    if value < 10 and exact_method_for_low_numbers:
        warnings.warn('As the sample is small, the exact method is used to calculate confidence intervals')
        upper_exact = exact_upper(value, (1 - confidence))
        lower_exact = exact_lower(value, (1 - confidence))
        if denominator and rate:
            return (lower_exact / denominator) * rate, (upper_exact / denominator) * rate
        else:
            return lower_exact, upper_exact
    elif value < 10:
        warnings.warn("As the sample is small and exact method not used, Byar's cannot be accurately calculated. Not-a-number will be returned")
        return np.nan, np.nan
    if denominator and rate:
        return (byars_lower(value, (1 - confidence)) / denominator) * rate, (byars_upper(value, (1 - confidence)) / denominator) * rate
    else:
        return byars_lower(value, (1 - confidence)), byars_upper(value, (1 - confidence))


def student_t_dist(value_count, st_dev, confidence=0.95):

    """Calculates the Student-t value to be used to create confidence intervals using the Student-t distribution.
    
    Args:
        value_count (int | float): The total value to calculate confidence intervals over.
        st_dev (int | float): Takes the standard deviation
        confidence (float): Takes a confidence interval (e.g. 0.95, 0.998)
    Returns:
        Student-t distribution value (float)
        
    """
    return abs(stats.t.ppf((1-confidence)/2, value_count - 1)) * st_dev / value_count**.5


def dobson_lower(value, total_count, var, confidence, multiplier):
    
    if total_count < 10:
        x = np.nan
    else:
        x = value + sqrt(var / total_count) * (byars_lower(total_count, confidence) - total_count) * multiplier
    
    return x
    

def dobson_upper(value, total_count, var, confidence, multiplier):
    
    if total_count < 10:
        x = np.nan
    else:
        x = value + sqrt(var / total_count) * (byars_upper(total_count, confidence) - total_count) * multiplier
    
    return x
   


