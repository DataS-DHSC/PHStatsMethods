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



def findxvalues(xvals):
    """Calculates mid-points of cumulative population for each quantile.
    
    Args:
        xvals: series name in input dataset that contains the grouped quantile populations
        
        Returns:
            Output field of mid-points
            
    """
    df = pd.DataFrame() #initialising dataframe
    
    df['prop'] = xvals / sum(xvals) #proportion
    df['cumprop'] = df['prop'].cumsum(skipna = False) #cumulative proportion
    
    df['lagged_cumprop'] = df['cumprop'].shift(1) #calling shift will move the lagged-cumporop column down one index, leaving NA in index 0.
    
    df['output'] = np.where(df['lagged_cumprop'].isna(), #where value is NA in lagged cumprop column
                            df['prop'] / 2,    # Proportion divided by 2 is the value used for output
                            df['prop'] / 2 + df['lagged_cumprop']) #otherwise value in output is Proportion divided by 2 plus value in lagged_cumprop
    
    return df['output']


    
    
    
    
    



