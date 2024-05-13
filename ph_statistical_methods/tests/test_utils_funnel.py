# -*- coding: utf-8 -*-
"""
Created on Wed May  1 08:18:14 2024

@author: Jack.Burden_DHSC
"""

import pytest
from utils_funnel import poisson_funnel

@pytest.mark.parametrize('obs, p, side, result', [(200, 0.025, 'low', 173.24086241121654),
                                                  (500, 0.001, 'high', 573.0274767209943)])
def test_poisson_funnel(obs, p, side, result):
    assert poisson_funnel(obs, p, side) == result