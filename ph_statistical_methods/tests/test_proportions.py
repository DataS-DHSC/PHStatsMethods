# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 17:07:04 2024

@author: Annabel.Westermann
"""

import pytest
from proportions import ph_proportion


@pytest.mark.slow
# command line: tests pytest -m slow
def test_rectangle(my_rectangle):
    assert my_rectangle == 6

@pytest.mark.skip(reason='This feature is broken')
def test_rectangle(my_rectangle):
    assert my_rectangle == 5


@pytest.mark.xfail(reason='Know cannot divide by 0')
def test_rectangle(my_rectangle):
    assert my_rectangle == 5
    
@pytest.mark.parametrize('side_length, expected_area', [2, 4])
def test_multiple_square_areas(side_length, expected_args):
    assert shapes.areas() == expected_area
    
# class TestProportion:
    
#     def __init__(self, length, width):
#         self.length = length
#         self.width = width
    
#     def setup_method(self, method):
#         print(f'Import data for {method}')
        
#     def teardown_method(self, method):
#         print(f'Tearing down {method}')
    
        
#     def test_two(self):
#         assert 2 == 1 + 1
#         return self.length == self.width