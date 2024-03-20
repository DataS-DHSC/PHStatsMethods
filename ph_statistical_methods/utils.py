# -*- coding: utf-8 -*-

from scipy.special import ndtri
from confidence_intervals import poisson_cis
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


def exact_lowercl(numerator, denominator, confidence = 0.95, multiplier = 100000):
    """
    Calculates exact lower confidence interval, takes in numerator, denominator, confidence, and multiplier.
    :param numerator:  numerator value, input as integer
    :param denominator: denomintaor value, input as integer
    :param confidence: confidence level used for calculation, set as default 0.95 for 95% confidence level.
    :param multiplier: multiplier level used for calulcation, default as 100000.

    """
   #calculates lower confidence interval
    lowercl = chi2(1-confidence)/2, 2*numerator/2/denominator * multiplier
    return lowercl

def exact_uppercl(numerator, denominator, confidence = 0.95, multiplier = 100000):
    """
    Calculates exact upper confidence interval, takes in numerator, denominator, confidence, and multiplier.
    :param numerator:  numerator value, input as integer
    :param denominator: denomintaor value, input as integer
    :param confidence: confidence level used for calculation, set as default 0.95 for 95% confidence level.
    :param multiplier: multiplier level used for calulcation, default as 100000.

    """
   #calculates upper confidence interval
    uppercl = chi2(confidence+(1-confidence)/2,2*numerator/2/denominator * multiplier)
    return uppercl



