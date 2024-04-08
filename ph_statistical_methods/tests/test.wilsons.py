# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:30:09 2024

@author: Jack.Burden_DHSC
"""

import pytest
from confidence_intervals import wilson, wilson_lower, wilson_upper

@pytest.mark.parametrize('num, denom, confidence, result' , [(20, 360, 0.95, 0.036248204600072345),
                                                             (550, 2400, 0.998, 0.20375892211705743)])
def test_wilson_lower(num, denom, confidence, result):
    assert wilson_lower(num, denom, confidence) == result
    
@pytest.mark.parametrize('num1, denom1, conf, res', [(30, 400, 0.95, 0.10504770626130437),
                                                     (76, 238, 0.998, 0.418131030603369)])

def test_wilson_upper(num1, denom1, conf, res):
    assert wilson_upper(num1, denom1, conf) == res