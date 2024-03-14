# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:19:46 2024

@author: Annabel.Westermann
"""

import pytest
from ..confidence_intervals import byars_lower

@pytest.mark.parametrize('value, confidence, result', [(100, 0.95, 99.04267017398342),
                                                       (200, 0.998, 199.63144417357614)])
def test_byars_lower(value, confidence, result):
    assert byars_lower(value, confidence) == result


@pytest.mark.skip(reason='This is already tested in the parameterized test above')
def test_byars_lower_3std():
    assert byars_lower(200, 0.998) == 199.63144417357614

