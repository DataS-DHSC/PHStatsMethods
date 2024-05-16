# -*- coding: utf-8 -*-
"""
Created on Wed May  1 08:18:14 2024

@author: Jack.Burden_DHSC
"""

import pytest
from utils_funnel import poisson_funnel, funnel_ratio_significance

@pytest.mark.parametrize('obs, p, side, result', [(200, 0.025, 'low', 173.24086241121654),
                                                  (500, 0.001, 'high', 573.0274767209943)])
def test_poisson_funnel(obs, p, side, result):
    assert poisson_funnel(obs, p, side) == result
    


@pytest.mark.parametrize('obs, expected, p, side, result', [(0, 10.0, 0.05, 'low', 0),  # Special case: obs is 0 and side is 'low'
                                                            (5, 10.0, 0.05, 'low', 0.45),  # Small sample size, 'low' side
                                                            (5, 10.0, 0.95, 'high', 1.17),  # Small sample size, 'high' side
                                                            (20, 15.0, 0.05, 'low', 1.29),  # Larger sample size, 'low' side
                                                            (25, 20.0, 0.95, 'high', 1.85)])  # Larger sample size, 'high' side
def test_funnel_ratio_significance(obs, expected, p, side, result):
    assert round(funnel_ratio_significance(obs, expected, p, side), 2) == result
