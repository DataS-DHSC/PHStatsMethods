# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:50:05 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from ISRate_aw import calculate_ISRate

data = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testdata_multiarea_isr')
results = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testresults_ISR')

test_ISR_lookup = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testdata_multiarea_lookup')

def test_default():
        df = calculate_ISRate(data, 'count', 'pop', 'refcount', 'refpop', group_cols='area').iloc[:, :7]
        assert_frame_equal(df, results.iloc[:3, :7], check_dtype=False)

def test_default_obs_total():
        df = calculate_ISRate(data, 'total_count', 'pop', 'refcount', 'refpop', group_cols='area',
                              obs_df = test_ISR_lookup, obs_join_left = 'area', obs_join_right = 'area').iloc[:, :7]
        assert_frame_equal(df, results.iloc[:3, :7], check_dtype=False)









data_multiarea = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testdata_multiarea')


est_multiarea   <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testdata_multiarea", col_names=TRUE) %>%
  group_by(area)
test_DSR_1976    <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testdata_1976",   col_names=TRUE)
test_err1        <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testdata_err1",   col_names=TRUE)
test_err2        <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testdata_err2",   col_names=TRUE) %>%
  group_by(area)
test_err3        <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testdata_err3",   col_names=TRUE)
test_DSR_results <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testresults_DSR", col_names=TRUE)
test_multigroup  <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testdata_multigroup", col_names=TRUE) %>%
  group_by(area,year)

test_ISR_results <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testresults_ISR", col_names=TRUE)
test_ISR_refdata <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="refdata",         col_names=TRUE)
test_ISR_ownref  <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testdata_multiarea_isr", col_names=TRUE) %>%
                      group_by(area)
test_ISR_lookup <- read_excel("tests/testthat/testdata_DSR_ISR.xlsx", sheet="testdata_multiarea_lookup", col_names=TRUE)
