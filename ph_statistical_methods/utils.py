# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
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


def FindXValues(xvals):

    df = pd.DataFrame()
    
    df['prop'] = xvals / sum(xvals)
    
    df['cumprop'] = df['prop'].cumsum(skipna = False)
    
    df['cumprop_lag'] = df['cumprop'].shift(1)
    
    df['output'] = np.where(df['cumprop_lag'].isna(), 
                            df['prop'] / 2, 
                            df['prop'] / 2 + df['cumprop_lag'])
    
    return df['output']


