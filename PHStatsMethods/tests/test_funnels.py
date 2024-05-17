# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:23:25 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from pandas.testing import assert_frame_equal

from ..funnels import calculate_funnel_limits, assign_funnel_significance, calculate_funnel_points

class TestFunnelLimits:
    
    path = Path(__file__).parent / 'test_data/testdata_funnels.xlsx'
    
    path = 'tests/test_data/testdata_funnels.xlsx'
    
    def test_conf_lim_prop(self):
        data = pd.read_excel(self.path, sheet_name='prop_inputs')
        results = pd.read_excel(self.path, sheet_name='prop_outputs')
        
        df = calculate_funnel_limits(data, 'numerator', denom_col='denominator', statistic = 'proportion', multiplier = 100, metadata=False)
        assert_frame_equal(df, results)
    
    def test_conf_lim_prop_axis_variation(self):
        data = pd.read_excel(self.path, sheet_name = 'prop_inputs')
        results_axis_var = pd.read_excel(self.path, sheet_name = 'prop_outputs_axis_var')
        
        df = calculate_funnel_limits(data[data['denominator'] < 31000], 'numerator', denom_col='denominator', 
                                      statistic = 'proportion', multiplier = 100, metadata=False)
        assert_frame_equal(df, results_axis_var)
    
    @pytest.mark.parametrize('ratio_type', ['count', 'isr'])
    def test_conf_lim_ratio(self, ratio_type):
        
        data = pd.read_excel(self.path, sheet_name = 'ratio_inputs')
        results = pd.read_excel(self.path, sheet_name = 'ratio_outputs')
        
        # ratio_type = 'count'
        df = calculate_funnel_limits(data, 'obs', denom_col='expected', statistic = 'ratio', 
                                      ratio_type = ratio_type, multiplier = 100, metadata=False)
        
        type_cols = [col for col in results.columns if ('isr' if ratio_type == 'count' else 'count') not in col]
        type_results = results[type_cols]
        type_results.columns = type_results.columns.str.replace(ratio_type, 'limit')
        
        assert_frame_equal(df, type_results)
        
        
    def test_conf_lim_rate_dsr(self):
        data = pd.read_excel(self.path, sheet_name = 'rate_inputs')
        results = pd.read_excel(self.path, sheet_name = 'rate_outputs')
        
        df = calculate_funnel_limits(data, 'ev', statistic = 'rate', rate = 'rate', 
                                      multiplier = 100000, rate_type = 'dsr', years_of_data = 3)
        
        assert_frame_equal(df, results)
    
    def test_conf_lim_rate_crude(self):
        data = pd.read_excel(self.path, sheet_name = 'rate_inputs')
        results = pd.read_excel(self.path, sheet_name = 'rate_outputs_2')
        
        data['ev'] = np.where(data['ev'] == data['ev'].max(), 5, data['ev'])
        
        df = calculate_funnel_limits(data, 'ev', statistic = 'rate', rate = 'rate',
                                      multiplier = 100000, rate_type = 'crude', years_of_data = 3)
        
        assert_frame_equal(df, results)
    
    def test_conf_lim_rate_crude_0_ev_denom(self):
        data = pd.read_excel(self.path, sheet_name = 'rate_inputs')
        results = pd.read_excel(self.path, sheet_name = 'rate_outputs_3')
        
        data = data[['ev', 'rate']]
        data['pop'] = 100000 * data['ev'] / data['rate']
        data['rate'] = np.where(data['ev'] == data['ev'].max(), 0, data['rate'])
        data['ev'] = np.where(data['ev'] == data['ev'].max(), 0, data['ev'])
        data = data[data['pop'] > data['pop'].max() / 2]
        
        df = calculate_funnel_limits(data, 'ev', denom_col = 'pop', statistic = 'rate', rate = 'rate',
                                      multiplier = 100000, rate_type = 'crude', years_of_data = 3)
        
        assert_frame_equal(df, results)


class TestFunnelSignif:
    
    path = Path(__file__).parent / 'test_data/testdata_funnels.xlsx'
    
    rate_data = pd.read_csv(path, sheet_name = 'rate_dsr_inputs')

    def test_signif_prop(self):
        data = pd.read_excel(self.path, sheet_name = 'prop_inputs.csv')
        
        df = assign_funnel_significance(data.drop('significance', axis=1), 
                                        'numerator', 'denominator', statistic = 'proportion')
        
        assert_frame_equal(df, data)
    
    def test_signif_ratio(self):
        data = pd.read_excel(self.path, 'ratio_inputs')
        
        df = assign_funnel_significance(data.drop('significance', axis=1), 
                                        'obs', 'expected', statistic = 'ratio')
        
        assert_frame_equal(df, data)
        
    def test_signif_rate_dsr_e5(self):
        result = self.rate_data[['count', 'rate_dsr', 'pop', 'dsr_per_100000_with_0']].rename(columns={'dsr_per_100000_with_0':'significance'})
        
        df = assign_funnel_significance(self.rate_data.iloc[:, :3], 'count', 'pop', rate = 'rate_dsr', statistic = 'rate',
                                        rate_type='dsr', multiplier = 100000)
        
        assert_frame_equal(df, result)
    
    def test_signif_rate_crude_e2(self):
        result = self.rate_data[['count', 'pop', 'rate_crude_per_100', 'crude_per_100_with_0']].rename(columns={'crude_per_100_with_0':'significance'})
        
        df = assign_funnel_significance(self.rate_data[['count', 'pop', 'rate_crude_per_100']], 'count', 'pop', rate = 'rate_crude_per_100', 
                                        statistic = 'rate', rate_type='crude', multiplier = 100)
        
        assert_frame_equal(df, result)
    
    
class TestFunnelPoints:
    
    path = Path(__file__).parent / 'test_data/testdata_funnels.xlsx'
    
    data = pd.read_excel(path, sheet_name = 'rate_inputs')
    
    def test_points_dsr_less_5(self):
        
        data = self.data.copy()
        data['ev'] = np.where(data['ev'] == data['ev'].max(), 5, data['ev'])
        
        df_in = data[['ev', 'rate']]
        df_out = data[['ev', 'rate', 'rate_chart', 'denom_derived']]
        
        df = calculate_funnel_points(df_in, 'ev', rate = 'rate', rate_type = 'dsr',
                                      years_of_data = 3, multiplier = 100000)
        
        assert_frame_equal(df, df_out)

















