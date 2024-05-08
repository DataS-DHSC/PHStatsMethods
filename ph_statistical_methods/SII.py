# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:15:36 2024

@author: Annabel.Westermann
"""
import pandas as pd
import warnings
from validation import format_args

df = pd.DataFrame({'area':['Area1']*10 + ['Area2'] * 10,
                   'decile':list(range(1,11)) * 2,
                   'population': [7291, 7997, 6105, 7666, 5790, 6934, 5918, 5974, 7147, 7534, 21675,
                                  20065, 19750, 24713, 20112, 19618, 22408, 19752, 18939, 19312],
                   'value': [75.9, 78.3, 83.8, 83.6, 80.5, 81.1, 81.7, 84.2, 80.6, 86.3, 70.5,
                              71.6, 72.5, 73.5, 73.1, 76.2, 78.7, 80.6, 80.9, 80],
                   'lowerCL': [72.7,75.3,80.9,80.2,77.1,78,79,81.4,75.8,83.2,
                               70.1,71.1,72,73.1, 72.7, 75.7, 78.2,80.1,80.4,79.5],
                   'upperCL': [79.1,81.4,86.8,87.1,83.8,84.2,84.4,86.9,85.4,
                                89.4,71,72.1,73.2,73.7,75.8,78.8,79.8,81.2,81.3,80.9],
                   'StandardError': [1.64,1.58,1.51,1.78,1.7,1.56,1.37,1.4,2.43,
                                     1.57,0.23,0.26,0.3,0.16,0.79,0.78,0.4,0.28,0.23,0.35]})

quantile = 'decile'
se = 'StandardError'
group_cols = ['area']

########

confidence, group_cols = format_args(confidence, group_cols)

if not isinstance(repetitions, int) or repetitions < 1000:
    raise TypeError("'Repetitions' must be an an integer bigger than 1000")
    
if se is None:
    if lowerCL is None or upperCL is None:
        raise TypeError("If 'se' is None, 'lowerCL' and 'upperCL' must be supplied")
    
# do various data number validation checks - all can't be less than 0 either I guess?

# can't be nulls for 'se' and 'population' or 'CL' - add this as a null check?

# unsure about converting factors to a string?
    
# Get quantiles
quantile_list = list(df[quantile].unique())
n_quantiles = len(quantile_list)

if n_quantiles < 5 or n_quantiles > 100:
    raise ValueError('Number of quantiles must be between 5 and 100')
elif n_quantiles >= 10:
    warnings.warn('Small values can make SII unstable when using a large number of quantiles')
    
# Remove records with missing essential data - negatives already filtered out by original checks?
if se is not None:
    df = df[df[se].notnull()]
else: 
    df = df[df[lowerCL].notnull() or df[upperCL].notnull()]
    
# Only use areas where there are valid areas - are grouped columns always the area though? - can this just be 1 group then?
valid_areas = df.groupby(group_cols)[quantile].size().reset_index()
valid_areas = valid_areas[valid_areas[quantile] == n_quantiles]
    
    
    
    
    
    
    
