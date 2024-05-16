# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:23:25 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from funnels import calculate_funnel_limits, assign_funnel_significance, calculate_funnel_points


def test_conf_lim_prop():
    data = pd.read_csv('tests/test_data/testdata_funnel_prop_inputs.csv')
    results = pd.read_csv('tests/test_data/testdata_funnel_prop_outputs.csv')
    
    df = calculate_funnel_limits(data, 'numerator', 'denominator', statistic = 'proportion', multiplier = 100, metadata=False)
    assert_frame_equal(df, results)

def test_conf_lim_prop_axis_variation():
    data = pd.read_csv('tests/test_data/testdata_funnel_prop_inputs.csv')
    results_axis_var = pd.read_csv('tests/test_data/testdata_funnel_prop_outputs_with_axis_variation.csv')
    
    df = calculate_funnel_limits(data[data['denominator'] < 31000], 'numerator', 'denominator', 
                                 statistic = 'proportion', multiplier = 100, metadata=False)
    assert_frame_equal(df, results_axis_var)


data = pd.read_csv('tests/test_data/testdata_funnel_ratio_inputs.csv')
results = pd.read_csv('tests/test_data/testdata_funnel_ratio_outputs.csv')

count_cols = [col for col in results.columns if 'isr' not in col]
isr_cols = [col for col in results.columns if 'count' not in col]

df = calculate_funnel_limits(data, 'obs', 'expected', statistic = 'ratio', 
                             ratio_type = 'count', multiplier = 100, metadata=False)

count_results = results[count_cols]
count_results.columns = count_results.columns.str.replace('count', 'limit')
isr_results = results[isr_cols]
isr_results.columns = isr_results.columns.str.replace('count', 'limit')

assert_frame_equal(df, count_results)

df = calculate_funnel_limits(data, 'obs', 'expected', statistic = 'ratio', 
                             ratio_type = 'count', multiplier = 100, metadata=False)

count_results.columns = count_results.columns.str.replace('count', 'limit')











