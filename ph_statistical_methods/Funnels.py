# -*- coding: utf-8 -*-
"""
Created on Tue May 14 21:28:21 2024

@author: Annabel.Westermann
"""

import pandas as pd
from math import floor, ceil

from utils_funnel import signif_floor, signif_ceiling



if statistic == 'rate':
    if rate_type == 'dsr':
        df['denom_derived'] = np.where(df[num_col] == 0, np.nan,
                                             multiplier * df[num_col] / df[rate])
    elif rate_type == 'crude':
        if denom_col is None:
            df['denom_derived'] = multiplier * df[num_col] / df[rate]
        else:
            df['denom_drived'] = np.where(df[num_col] == 0, df[denom_col],
                                          multiplier * df[num_col] * df[rate])
else:
    df['denom_derived'] = df[denom_col]

# aggregate data to calculate baseline average for funnel plot
av = df[num_col].sum(skipna=False) / df['derived_denom'].sum()
min_denom = df['derived_denom'].min()
max_denom = df['derived_denom'].max()

# calcuate min and max x-axis denominator
if max_denom > 2 * min_denom:
    axis_min = 0
else:
    axis_min = signif_floor(min_denom / years_of_data) * years_of_data if statistic == 'rate' else signif_floor(min_denom)
    
axis_max = signif_ceiling(max_denom / years_of_data) if statistic == 'rate' else signif_ceiling(max_denom)

# useful column headers
col_headers = {'proportion': 'Population', 'ratio': 'Observed_events', 'rate': 'Events'}

if statistic == 'rate':
    axis_min = floor(axis_min * av)
    axis_max = ceiling(axis_max * av)

# populate table of 100 rows to generate funnel line plot data for chart
first_col = [max([1, axis_min])]
for j in range(2, 101):
    offset = j - 1 if statistic == 'rate' else j
    k = max([round((axis_max/first_col[-1])**(1 / (101-offset)) * first_col[-1]), first_col[-1] + 1])
    first_col.append(k)