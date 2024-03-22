# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:30:09 2024

@author: Jack.Burden_DHSC
"""

import pytest
from confidence_intervals import wilson, wilson_lower, wilson_upper

#checking for correct result for wilson lower at 95% confidence
def test_wilson_lower95():
    assert wilson_lower(20, 360, 0.95) ==  0.036248204600072345

#checking for correct result for wilson lower at 99.8% confidence
def test_wilson_lower99_8():
    assert wilson_lower(550, 2400, 0.998) == 0.20375892211705743

#checking for correct result for wilson upper at 95% confidence
def test_wilson_upper95():
    assert wilson_upper(30, 400, 0.95) == 0.10504770626130437

#checking for correct reuslt for wilson upper at 99.85 confidence
def test_wilson_upper99_8():
    assert wilson_upper(76, 238, 0.998) == 0.418131030603369