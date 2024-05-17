# -*- coding: utf-8 -*-
"""
Created on Wed May  1 08:18:14 2024

@author: Jack.Burden_DHSC
"""

import pytest
from ..utils_funnel import poisson_funnel, funnel_ratio_significance, sigma_adjustment

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


@pytest.mark.parametrize("p, pop, av_prop, side, mult, result", [(0.975, 100000, 0.9, "low", 100, 89.81406149030842),
                                                                 (0.999, 300000, 0.85, "high", 1000, 852.0145849882799)])
def test_sigma(p, pop, av_prop, side, mult, result):
    assert sigma_adjustment(p, pop, av_prop, side, mult) == result
