# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:19:46 2024

@author: Annabel.Westermann
"""

import pytest
from confidence_intervals import byars_lower, wilson_lower, wilson_upper

@pytest.mark.parametrize('value, confidence, result', [(100, 0.95, 99.04267017398342),
                                                       (200, 0.998, 199.63144417357614)])
def test_byars_lower(value, confidence, result):
    assert byars_lower(value, confidence) == result


@pytest.mark.skip(reason='This is already tested in the parameterized test above')
def test_byars_lower_3std():
    assert byars_lower(200, 0.998) == 199.63144417357614


@pytest.mark.parametrize('numerator, denominator. confidence, result', [(20, 360, 0.95, 0.0362482),
                                                                        (550, 2400, 0.95, 0.2127923)])
def test_wilson_lower(numerator, denominator, confidence, result):
    assert wilson_lower(numerator, denominator, confidence) == result


