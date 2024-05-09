# -*- coding: utf-8 -*-

from scipy.special import ndtri
from scipy.stats import chi2
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

<<<<<<< HEAD
def findxvalues(xvals, no_quantiles):
    """Calculates mid-points of cumulative population for each quantile.
    
    Args:
        xvals: field name in input Dataset that contains the quantile populations
        no_quantiles: (integer) number of quantiles supplied in dataset for SII
        
        Returns:
            Output field of mid-points
            
    """
    df = pd.DataFrame({'prop': [0.0] * no_quantiles,
                       'cumprop': [0.0] * no_quantiles,
                       'output': [0.0] * no_quantiles})

    xvals = np.array(xvals)
    
    df['prop'] = xvals / sum(xvals)
    df['cumprop'] = df['prop'].cumsum()
    df['output'] = #np.where(df['cumprop'].shift(1).isna(), df['prop'] / 2, df['prop'] / 2 + df['cumprop'].fillna(0) / 2)
    
    return df['output']


    
    
    
    
    






=======
>>>>>>> Dev
