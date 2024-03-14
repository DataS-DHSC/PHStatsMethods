# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:19:46 2024

@author: Annabel.Westermann
"""

from confidence_intervals import byars_lower

def test_byars_lower():
    assert byars_lower(100) == 81.36210549052788


from utils import funnel_ratio_significance

def test_funnel_ratio_significance():
    assert funnel_ratio_significance(5, 15, 0.01, 'high') == 0.37999398868094036