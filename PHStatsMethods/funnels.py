# -*- coding: utf-8 -*-
"""
Created on Tue May 14 21:28:21 2024

@author: Annabel.Westermann
"""

import pandas as pd
import numpy as np
from math import floor, ceil

from .validation import metadata_cols, validate_data
from .utils_funnel import signif_floor, signif_ceiling, sigma_adjustment, poisson_funnel, funnel_ratio_significance


def calculate_funnel_limits(df, num_col, statistic, multiplier, denom_col = None, metadata = True, 
                            rate = None, rate_type = None, ratio_type = None, years_of_data = None):
    """Calculates control limits adopting a consistent method as per the Fingertips Technical Guidance

    Args:
        df: DataFrame containing the data to calculate control limits for.
        num_col (str): Name of column containing observed number of cases in the sample
                (the numerator of the population).
        statistic (str): type of statistic to inform funnel calculations: 'proportion', 'rate', or 'ratio'
        multiplier (int): multiplier used to express the final values (e.g. 100 = percentage)
        denom_col (str): Name of column containing number of cases in sample 
                (the denominator of the population).
        metadata (bool): Whether to include information on the statistic and confidence interval methods.
        rate (str): column name containing the 'rate'.
        rate_type (str): if statistic is 'rate', specify either 'dsr' or 'crude'.
        ratio_type (str): if statistic is 'ratio', specify either 'count' or 'isr' (indirectly standardised ratio).
        years_of_data (int): number of years the data represents; this is required if statistic is 'ratio'

    Returns:
        DataFrame of calculated confidence limits.
        
    """
    
    df = validate_data(df, num_col, denom_col = denom_col, metadata = metadata)
    
    if (df[num_col].isna()).any():
        raise ValueError('Numerators must provided for all records, even when their values are 0')
        
    if denom_col is not None:
        if (df[denom_col].isna()).any():
            raise ValueError('Numerators must provided for all records, even when their values are 0')
    
    if statistic not in ['rate', 'proportion', 'ratio']:
        raise ValueError("'statistic' must be either 'proportion', 'ratio' or 'rate")
    
    if statistic == 'rate':
        if rate is None or rate_type is None or years_of_data is None or multiplier is None:
            raise TypeError("'rate', 'rate_type', 'years_of_data' and 'multiplier' are required for rate statistics")
        if rate_type not in ['dsr', 'crude']:
            raise ValueError("only 'dsr' and 'crude' are valid rate_types")
        
        if denom_col is None and (df[rate].isna()).any():
            raise ValueError("For rates, 'rate' must be provided for all records even if the rate is 0 or a denominator must be provided")
        
        if denom_col is None and (df[num_col] == 0).any():
            raise ValueError("For rates, where there are 0 events for a record, 'denom_col' must be provided")
    
    elif statistic in ['proportion', 'ratio']:
        if denom_col is None:
            raise TypeError("'denom_col' must be given for 'proportion' and 'ratio' statistics")
            
    elif statistic == 'ratio':
        if ratio_type is None or ratio_type not in ['isr', 'count']:
            raise ValueError("'ratio_type' must be given for ratio statistics: 'isr' or 'count'")
            
    
    if statistic == 'rate':
        if rate_type == 'dsr':
            df['denom_derived'] = np.where(df[num_col] == 0, np.nan,
                                                 multiplier * df[num_col] / df[rate])
        elif rate_type == 'crude':
            if denom_col is None:
                df['denom_derived'] = multiplier * df[num_col] / df[rate]
            else:
                df['denom_derived'] = np.where(df[num_col] == 0, df[denom_col],
                                              multiplier * df[num_col] / df[rate])
    else:
        df['denom_derived'] = df[denom_col]
    
    # aggregate data to calculate baseline average for funnel plot
    av = df[num_col].sum(skipna=False) / df['denom_derived'].sum()
    min_denom = df['denom_derived'].min()
    max_denom = df['denom_derived'].max()
    
    # calcuate min and max x-axis denominator
    if max_denom > 2 * min_denom:
        axis_min = 0
    else:
        axis_min = signif_floor(min_denom / years_of_data) * years_of_data if statistic == 'rate' else signif_floor(min_denom)
        
    axis_max = signif_ceiling(max_denom / years_of_data) * years_of_data if statistic == 'rate' else signif_ceiling(max_denom)
    
    # useful column headers
    col_headers = {'proportion': 'Population', 'ratio': 'Observed_events', 'rate': 'Events'}
    col = col_headers.get(statistic)
    
    if statistic == 'rate':
        axis_min = floor(axis_min * av)
        axis_max = ceil(axis_max * av)
    
    # populate table of 100 rows to generate funnel line plot data for chart
    first_col = [max([1, axis_min])]
    for j in range(2, 101):
        offset = j - 1 if statistic == 'ratio' else j
        k = max([round((axis_max/first_col[-1])**(1 / (101-offset)) * first_col[-1]), first_col[-1] + 1])
        first_col.append(k)
    
    t = pd.DataFrame({col: first_col})
    
    # there doesnt seem any advantage doing the grouping then ungrouping in the R?
    if statistic == 'proportion':
        t['lower_2s_limit'] = t[col].apply(lambda x: max([0, sigma_adjustment(0.975, x, av, 'low', multiplier)]))
        t['upper_2s_limit'] = t[col].apply(lambda x: min([100, sigma_adjustment(0.975, x, av, 'high', multiplier)]))
        
        t['lower_3s_limit'] = t[col].apply(lambda x: max([0, sigma_adjustment(0.999, x, av, 'low', multiplier)]))
        t['upper_3s_limit'] = t[col].apply(lambda x: min([100, sigma_adjustment(0.999, x, av, 'high', multiplier)]))
        
        t['baseline'] = av * multiplier
    
    elif statistic == 'ratio':
        t['lower_2s_exp_events'] = t[col].apply(lambda x: poisson_funnel(x, 0.025, 'high'))
        t['lower_2s_limit'] = t[col] / t['lower_2s_exp_events']
        t['upper_2s_exp_events'] = t[col].apply(lambda x: poisson_funnel(x, 0.025, 'low'))
        t['upper_2s_limit'] = t[col] / t['upper_2s_exp_events']
        
        t['lower_3s_exp_events'] = t[col].apply(lambda x: poisson_funnel(x, 0.001, 'high'))
        t['lower_3s_limit'] = t[col] / t['lower_3s_exp_events']
        t['upper_3s_exp_events'] = t[col].apply(lambda x: poisson_funnel(x, 0.001, 'low'))
        t['upper_3s_limit'] = t[col] / t['upper_3s_exp_events']
        
        for col in [col for col in t.columns if 'limit' in col]:
            if ratio_type == 'count':
                t[col] = t[col] - 1
            elif ratio_type == 'isr':
                t[col] = t[col] * 100
        
    elif statistic == 'rate':
        t['lower_2s_population_1_year'] = t[col].apply(lambda x: (poisson_funnel(x, 0.025, 'high'))) / av
        t['lower_2s_limit'] = t[col] / t['lower_2s_population_1_year']
        t['upper_2s_population_1_year'] = t[col].apply(lambda x: (poisson_funnel(x, 0.025, 'low'))) / av
        t['upper_2s_limit'] = t[col] / t['upper_2s_population_1_year']
        
        t['lower_3s_population_1_year'] = t[col].apply(lambda x: (poisson_funnel(x, 0.001, 'high'))) / av
        t['lower_3s_limit'] = t[col] / t['lower_3s_population_1_year']
        t['upper_3s_population_1_year'] = t[col].apply(lambda x: (poisson_funnel(x, 0.001, 'low'))) / av
        t['upper_3s_limit'] = t[col] / t['upper_3s_population_1_year']
        
        t['baseline'] = av * multiplier
        
        for col in [col for col in t.columns if 'limit' in col]:
            t[col] = t[col] * multiplier
        for col in [col for col in t.columns if '1_year' in col]:
            t[col] = t[col] / years_of_data
        
    if metadata:
        if statistic == 'proportion':
            stat = statistic
        elif statistic == 'ratio':
            stat = f'{statistic} ({ratio_type})'
        elif statistic == 'rate':
            stat = f'{statistic} ({rate_type} per {multiplier})'
            
        t = metadata_cols(t, stat, None, 'Wilson' if statistic == 'proportion' else 'Poisson')
        
    return t
        


def assign_funnel_significance(df, num_col, statistic, denom_col = None, rate = None, rate_type = None, multiplier = None):
    """Identifies whether each value in a dataset falls outside of 95 and/or 99.8 percent control limits based on the 
    aggregated average value across the whole dataset as an indicator of statistically significant difference.

    Args:
        df: DataFrame containing the data to calculate control limits for.
        num_col (str): Name of column containing observed number of cases in the sample
                (the numerator of the population).
        statistic (str): type of statistic to inform funnel calculations: 'proportion', 'rate', or 'ratio'
        denom_col (str): Name of column containing number of cases in sample 
                (the denominator of the population).
        metadata (bool): Whether to include information on the statistic and confidence interval methods.
        rate (str): column name containing the 'rate'.
        rate_type (str): if statistic is 'rate', specify either 'dsr' or 'crude'.
        multiplier (int): multiplier the rate is normalised with (i.e. per 100000) only required when statistic is 'rate'.

    Returns:
        DataFrame of calculated significance levels.
        
    """
    
    if statistic not in ['rate', 'proportion', 'ratio']:
        raise ValueError("'statistic' must be either 'proportion', 'ratio' or 'rate")
        
    df = validate_data(df, num_col, denom_col = denom_col)
    
    if (df[num_col].isna()).any():
        raise ValueError('Numerators must provided for all records, even when their values are 0')
        
    if denom_col is not None:
        if (df[denom_col].isna()).any():
            raise ValueError('Numerators must provided for all records, even when their values are 0')
    
    if statistic not in ['rate', 'proportion', 'ratio']:
        raise ValueError("'statistic' must be either 'proportion', 'ratio' or 'rate")
    
    if statistic == 'rate':
        if rate is None or rate_type is None or multiplier is None:
            raise TypeError("'rate', 'rate_type', and 'multiplier' are required for rate statistics")
        
        elif rate_type not in ['dsr', 'crude']:
            raise ValueError("only 'dsr' and 'crude' are valid rate_types")
        
        elif denom_col is None and (df[rate].isna()).any():
            raise ValueError("For rates, 'rate' must be provided for all records even if the rate is 0 or a denominator must be provided")
            
        if denom_col is None and (df[num_col] == 0).any():
            raise ValueError("For rates, where there are 0 events for a record, 'denom_col' must be provided")
    
    elif statistic in ['proportion', 'ratio']:
        if denom_col is None:
            raise TypeError("'denom_col' must be given for 'proportion' and 'ratio' statistics")
            
    if statistic == 'proportion':
        if (df[num_col] > df[denom_col]).any():
            raise ValueError('Numerators must be less than or equal to the denominator for a proportion statistic')  
            
        av = df[num_col].sum() / df[denom_col].sum() # don't need skipna here as validation ensures no nulls
        
        df['significance'] = np.where(df[num_col] / df[denom_col] < df[denom_col].apply(lambda x: sigma_adjustment(0.999, x, av, 'low', 1)), 'Low (0.001)',
                             np.where(df[num_col] / df[denom_col] < df[denom_col].apply(lambda x: sigma_adjustment(0.975, x, av, 'low', 1)), 'Low (0.025)',
                             np.where(df[num_col] / df[denom_col] > df[denom_col].apply(lambda x: sigma_adjustment(0.999, x, av, 'high', 1)), 'High (0.001)',
                             np.where(df[num_col] / df[denom_col] > df[denom_col].apply(lambda x: sigma_adjustment(0.975, x, av, 'high', 1)), 'High (0.025)',
                                      'Not significant'))))
    
    elif statistic == 'ratio':
        df['significance'] = np.where(1 < df.apply(lambda x: funnel_ratio_significance(x[num_col], x[denom_col], 0.998, 'low'), axis=1), 'High (0.001)',
                             np.where(1 < df.apply(lambda x: funnel_ratio_significance(x[num_col], x[denom_col], 0.95, 'low'), axis=1), 'High (0.025)',
                             np.where(1 > df.apply(lambda x: funnel_ratio_significance(x[num_col], x[denom_col], 0.998, 'high'), axis=1), 'Low (0.001)',
                             np.where(1 > df.apply(lambda x: funnel_ratio_significance(x[num_col], x[denom_col], 0.95, 'high'), axis=1), 'Low (0.025)',
                                      'Not significant'))))
        
    elif statistic == 'rate':
        if rate_type == 'dsr':
            df['denom_derived'] = np.where(df[num_col] == 0, np.nan, df[num_col] / df[rate] * multiplier)
        elif rate_type == 'crude':
            if denom_col is None:
                df['denom_derived'] = multiplier * df[num_col] / df[rate]
            else:
                df['denom_derived'] = np.where(df[num_col] == 0, df[denom_col], multiplier * df[num_col] / df[rate])
            
        weighted_av = df[num_col].sum() / df['denom_derived'].sum() # this already ignores nulls
        
        df['significance'] = np.where(weighted_av < df.apply(lambda x: funnel_ratio_significance(x[num_col], x['denom_derived'], 0.998, 'low'), axis=1), 'High (0.001)',
                             np.where(weighted_av < df.apply(lambda x: funnel_ratio_significance(x[num_col], x['denom_derived'], 0.95, 'low'), axis=1), 'High (0.025)',
                             np.where(weighted_av > df.apply(lambda x: funnel_ratio_significance(x[num_col], x['denom_derived'], 0.998, 'high'), axis=1), 'Low (0.001)',
                             np.where(weighted_av > df.apply(lambda x: funnel_ratio_significance(x[num_col], x['denom_derived'], 0.95, 'high'), axis=1), 'Low (0.025)',
                                      'Not significant'))))
        df = df.drop('denom_derived', axis=1)
        
        if rate_type == 'dsr':
            df['significance'] = np.where(df[num_col] < 10, 'Not applicable for events less than 10 for DSRs', df['significance'])
            
    return df
        


def calculate_funnel_points(df, num_col, rate, rate_type, denom_col = None,
                            multiplier = 100000, years_of_data = 1):
    """For rate-based funnels: Derive rate and annual population values for charting based. Process removes rates where the 
    rate type is dsr and the number of observed events are below 10.

    Args:
        df: DataFrame containing the data to calculate control limits for.
        num_col (str): Name of column containing observed number of cases in the sample
                (the numerator of the population).
        statistic (str): type of statistic to inform funnel calculations: 'proportion', 'rate', or 'ratio'
        denom_col (str): Name of column containing number of cases in sample 
                (the denominator of the population).
        metadata (bool): Whether to include information on the statistic and confidence interval methods.
        years_of_data (int): number of years the data represents
        multiplier (int): multiplier the rate is normalised with (i.e. per 100000).

    Returns:
        DataFrame of calculated funnel points. First will have the same name as the rate field,
        with the suffix '_chart', the second will be called denominator_derived.
        
    """
    
    df = validate_data(df, num_col, denom_col = denom_col)
    
    if rate_type not in ['dsr', 'crude']:
        raise ValueError("only 'dsr' and 'crude' are valid rate_types")
    
    if (df[rate].isna()).any():
        raise ValueError("For rates, 'rate' must be provided for all records even if the rate is 0")
        
    if denom_col is None and (df[num_col] == 0).any():
        raise ValueError("For rates, where there are 0 events for a record, 'denom_col' must be provided")
    
    if rate_type == 'dsr':
        df[f'{rate}_chart'] = np.where(df[num_col] < 10, np.nan, 
                                       df[rate])
        df['denom_derived'] = np.where(df[num_col] < 10, np.nan, 
                                       (multiplier * df[num_col] / df[rate]) / years_of_data)
    
    elif rate_type == 'crude':
        df[f'{rate}_chart'] = df[rate]
        
        if denom_col is None:
            df['denom_derived'] = (multiplier * df[num_col] / df[rate]) / years_of_data
        else:
            df['denom_derived'] = np.where(df[num_col] == 0, df[denom_col] / years_of_data,
                                           (multiplier * df[num_col] / df[rate]) / years_of_data)
    
    return df
            
    
