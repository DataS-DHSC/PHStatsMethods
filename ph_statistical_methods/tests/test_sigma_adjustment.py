# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:08:49 2024

@author: Jack.Burden_DHSC
"""
from utils_funnel import sigma_adjustment
import pytest


@pytest.mark.parametrize("p, pop, av_prop, side, mult, result", [(0.975, 100000, 0.9, "low", 100, 89.81406149030842)])
def test_sigma(p, pop, av_prop, side, mult, result):
    assert sigma_adjustment(p, pop, av_prop, side, mult) == result


@pytest.mark.parametrize("p, pop, av_prop, side, mult, result", [(0.999, 300000, 0.85, "high", 1000, 852.0145849882799)])
def test_sigma_high(p, pop, av_prop, side, mult, result):
    assert sigma_adjustment(p, pop, av_prop, side, mult) == result
                         