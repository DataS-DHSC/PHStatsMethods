# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 17:07:04 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from proportions import ph_proportion


@pytest.fixture
def setup_data():
    yield pd.read_excel('tests/test_data/testdata_Proportion.xlsx', sheet_name = 'testdata_Prop').iloc[:,:-1]

@pytest.fixture
def setup_data_g():
    yield pd.read_excel('tests/test_data/testdata_Proportion.xlsx', sheet_name = 'testdata_Prop_g')


def test_default(setup_data):
    df = ph_proportion(setup_data.iloc[:8, :3], 'Numerator', 'Denominator').drop(['Confidence'], axis=1)
    assert_frame_equal(df, setup_data.iloc[:8, [0,1,2,3,4,5,8,10]])
    
def test_default_2ci(setup_data):
    df = ph_proportion(setup_data.iloc[:8, :3], 'Numerator', 'Denominator', confidence = [0.95, 0.998])
    assert_frame_equal(df, setup_data.iloc[:8, :])

def test_percentage(setup_data):
    
df = pd.read_excel('tests/test_data/testdata_Proportion.xlsx', sheet_name = 'testdata_Prop').iloc[:,:-1]
df1 = ph_proportion(df.iloc[8:16, :3], 'Numerator', 'Denominator', multiplier = 100).drop(['Confidence'], axis=1)
df2 = df.iloc[8:16, [0,1,2,3,4,5,8,10]]
assert_frame_equal(df1, df2)
#   expect_equal(data.frame(select(phe_proportion(slice(test_Prop,9:16)[1:3], Numerator, Denominator,
#                               multiplier = 100, type="full"),1:6,8:9)),
#                data.frame(select(slice(test_Prop,9:16),1:6,9:10)),
#                ignore_attr = TRUE, info="test full, percentage")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator,
#                               multiplier = 1, type="standard")),
#                data.frame(select(slice(test_Prop,1:8),1:6)),
#                ignore_attr = TRUE, info="test standard")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator,
#                                          multiplier = 1, confidence = c(0.95,0.998), type="standard")),
#                data.frame(select(slice(test_Prop,1:8),1:8)),
#                ignore_attr = TRUE, info="test standard 2 CIs")

#   expect_equal(data.frame(select(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator,
#                               type="full", confidence=99.8), 1:6,8:9)),
#                data.frame(select(slice(test_Prop,1:8),1:4,7:10)),
#                ignore_attr = TRUE, info="test confidence")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator, type="value")),
#                data.frame(select(slice(test_Prop,1:8),1:4)),
#                ignore_attr = TRUE, info="test value")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator,
#                                          confidence = c(0.95,0.998), type="value")),
#                data.frame(select(slice(test_Prop,1:8),1:4)),
#                ignore_attr = TRUE, info="test value 2 CIs")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator, type="lower")),
#                data.frame(select(slice(test_Prop,1:8),1:3,5)),
#                ignore_attr = TRUE, info="test lower")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator,
#                                          confidence = c(0.95,0.998), type="lower")),
#                data.frame(select(slice(test_Prop,1:8),1:3,5,7)),
#                ignore_attr = TRUE, info="test lower 2 CIs")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator, type="upper")),
#                data.frame(select(slice(test_Prop,1:8),1:3,6)),
#                ignore_attr = TRUE, info="test upper")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator,
#                                          confidence = c(0.95,0.998), type="upper")),
#                data.frame(select(slice(test_Prop,1:8),1:3,6,8)),
#                ignore_attr = TRUE, info="test upper 2 CIs")

#   expect_equal(arrange(data.frame(select(phe_proportion(filter(test_Prop,Area %in% c("Area09","Area10","Area11"))[1:3],
#                                                  Numerator, Denominator, type="full"),1:6,8:9)), Area),
#                arrange(data.frame(select(filter(test_Prop,Area %in% c("Area09","Area10","Area11")),1:6,9:10)), Area),
#                ignore_attr = TRUE, info="test NAs")

#   expect_equal(arrange(data.frame(phe_proportion(slice(test_Prop_g,1:8)[1:3], Numerator, Denominator, type="standard")), Area),
#                arrange(select(data.frame(test_Prop_g_results[1:6]),1:6),Area),
#                ignore_attr = TRUE, info="test grouped")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop,1:8)[1:3], Numerator, Denominator, confidence = c(0.95, 0.998)))[1:6],
#                data.frame(select(slice(test_Prop,1:8),1:9))[1:6],
#                ignore_attr = TRUE, info="test two CIs 95%")

#   expect_equal(data.frame(select(phe_proportion(slice(test_Prop,9:16)[1:3], Numerator, Denominator,
#                                                 multiplier = 100, confidence = c(0.95, 0.998)),1:4,7,8)),
#                data.frame(select(slice(test_Prop,9:16),1:4,7:8)),
#                ignore_attr = TRUE, info="test two CIs 99.8%")

#   expect_equal(data.frame(select(phe_proportion(slice(test_Prop,9:16)[1:3], Numerator, Denominator,
#                                                 confidence = c(0.95, 0.998)),9)),
#                data.frame(confidence = rep("95%, 99.8%",8), stringsAsFactors = FALSE),
#                ignore_attr = TRUE, info="test two CIs, metadata")

#   expect_equal(data.frame(phe_proportion(slice(test_Prop_g_results,1:8)[1:3], Numerator, Denominator,
#                                                 confidence = NA)),
#                data.frame(select(slice(test_Prop_g_results_no_CI,1:8),1:4,8)),
#                ignore_attr = TRUE, info="test no CIs")

# })








# def test

# @pytest.mark.slow
# # command line: tests pytest -m slow
# def test_rectangle(my_rectangle):
#     assert my_rectangle == 6

# @pytest.mark.skip(reason='This feature is broken')
# def test_rectangle(my_rectangle):
#     assert my_rectangle == 5


# @pytest.mark.xfail(reason='Know cannot divide by 0')
# def test_rectangle(my_rectangle):
#     assert my_rectangle == 5
    
# @pytest.mark.parametrize('side_length, expected_area', [(2, 4), (5,3), (8,2)])
# def test_multiple_square_areas(side_length, expected_args):
#     assert shapes.areas() == expected_area
    
    

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