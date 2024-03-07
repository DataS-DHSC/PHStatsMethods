# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:19:46 2024

@author: Annabel.Westermann
"""

from confidence_intervals import byars_lower

def test_byars_lower():
    assert byars_lower(100) == 81.36210549052788


