# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:15:36 2024

@author: Annabel.Westermann
"""
import pandas as pd
import warnings
import numpy as np
from scipy.stats import norm
from validation import format_args
from utils import FindXValues

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
group_cols = ['area'] # must pass a group
confidence = 0.95
value_type = 'other'
denom_col = 'population'
value = 'value'
repetitions = 2000

########

df = df.copy().reset_index()

confidence, group_cols = format_args(confidence, group_cols)

if value_type not in ['rate', 'proportion', 'other']:
    raise ValueError("'value_type' must be either 'rate', 'proportion', or 'other'")

if not isinstance(repetitions, int) or repetitions < 1000:
    raise TypeError("'Repetitions' must be an an integer bigger than 1000")
    
if se is None:
    if lowerCL is None or upperCL is None:
        raise TypeError("If 'se' is None, 'lowerCL' and 'upperCL' must be supplied")
    
# do various data number validation checks - all can't be less than 0 either I guess?

# there does not need to be a value if proportions and counts are provided - check?

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
    valid_complete = df[df[se].notnull()]
else: 
    valid_complete = df[df[lowerCL].notnull() or df[upperCL].notnull()]
    
# Only use areas where there are valid areas - are grouped columns always the area though? - can this just be 1 group then?
valid_areas = valid_complete.groupby(group_cols)[quantile].size().reset_index()
valid_areas = valid_areas[valid_areas[quantile] == n_quantiles]
# does this only allow 1 grouping column?
valid_deciles = pd.concat([valid_areas] * n_quantiles, ignore_index = True).sort_values(by = group_cols)
valid_deciles[quantile] = quantile_list * len(valid_areas)
#valid_deciles['n'] = n_quantiles

if len(valid_deciles) != len(df):
    warnings.warn('Some records have been removed due to incomplete or invalid data')
    
pops_prep = valid_deciles.merge(df, how = 'left', on = group_cols + [quantile])

# calculate indicator value
if value is not None:
    pops_prep = pops_prep.rename(columns = {value: 'Value'})
else:
    pops_prep['Value'] = pops_prep[num_col] / pops_prep[denom_col]
    
# Transform value if value is a rate or proportion
if value_type == 'rate':
    pops_prep['Value'] = np.log(pops_prep['Value'])
    if se is not None:
        pops_prep[lowerCL] = np.log(pops_prep[lowerCL])
        pops_prep[upperCL] = np.log(pops_prep[upperCL])
        
elif value_type == 'proportion':
    pops_prep['Value'] = np.log(pops_prep['Value'] / (1 - pops_prep['Value'])) # this means value must be bigger than 1?
    if se is not None:
        pops_prep[lowerCL] = np.log(pops_prep[lowerCL] / (1 - pops_prep[lowerCL]))
        pops_prep[upperCL] = np.log(pops_prep[upperCL] / (1 - pops_prep[upperCL]))
    
# Calculate standard error
z = norm.ppf(0.975)

if se is not None:
    pops_prep = pops_prep.rename(columns = {se: 'se_calc'})
else:
    pops_prep['se_calc'] = (pops_prep[upperCL] - pops_prep[lowerCL]) / z / 2

# sort values within groups in quantile ascending order for FindXValues
data = pops_prep.sort_values(by = group_cols + [quantile])
    
# writing it like this to keep calculations and resulting series in place?
if group_cols is None:
    data['a_vals'] = data[denom_col] / data[denom_col].sum()
    data['b_vals'] = FindXValues(data[denom_col])
else:
    data['a_vals'] = data.groupby(group_cols).apply(lambda x: x[denom_col] / x[denom_col].sum()).reset_index()[denom_col]
    data['b_vals'] = data.groupby(group_cols)[denom_col].apply(lambda x: FindXValues(x)).reset_index()[denom_col]



# Calculate sqrt and bsqrt and un-transformed y value for regression
data['sqrt_a'] = np.sqrt(data['a_vals'])
data['b_sqrt_a'] = data['b_vals'] * data['sqrt_a']

if transform == True or value_type == 'other':
    data['value_transform'] = data['Value']
else:
    data['value_transform'] = np.where(value_type == 'rate', np.exp(data['Value']), # does it need to be a float or do integers work?
                                   np.exp(data['Value']) / (1 + np.exp(data['Value'])))
    
data['yvals'] = data['sqrt_a'] * data['value_transform']

# Calculate confidence interval for SII via simulation

    
