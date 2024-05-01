# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 17:34:08 2024

@author: Annabel.Westermann
"""

def poisson_cis(z, x_a, x_b):
    """
    Calculates the cumulative dribution function of a Poisson distribution.
    
    :param z: The average rate of occurence of events within a fixed interval of time or space.
    :param x_a: The lower bound of the interval to be used in the calculation.
    :param x_b: The upper bound of the interval to be used in the calculation.
    :return: The cumulative probability of a number of events falling between the intervals given the average rate.
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


