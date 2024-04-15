# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:06:36 2024

@author: T.Vikneswaran_DHSC
"""

import pytest
from utils import funnel_ratio_significance

@pytest.mark.parametrize('obs, expected, p, side, result', [
    (0, 10.0, 0.05, 'low', 0),  # Special case: obs is 0 and side is 'low'
    (5, 10.0, 0.05, 'low', 0.45),  # Small sample size, 'low' side
    (5, 10.0, 0.95, 'high', 1.17),  # Small sample size, 'high' side
    (20, 15.0, 0.05, 'low', 1.29),  # Larger sample size, 'low' side
    (25, 20.0, 0.95, 'high', 1.85)  # Larger sample size, 'high' side
])


def test_funnel_ratio_significance(obs, expected, p, side, result):
    assert round(funnel_ratio_significance(obs, expected, p, side), 2) == result

@pytest.mark.skip(reason="Special cases are tested in the parameterised test above")
def test_funnel_ratio_significance_special_case():
    assert funnel_ratio_significance(0, 10.0, 0.05, 'low') == 0


