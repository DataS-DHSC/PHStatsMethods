# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:50:05 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from ISRate import calculate_ISRate

data = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testdata_multiarea_isr')
data_multiarea = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testdata_multiarea')

results = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name = 'testresults_ISR')



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
