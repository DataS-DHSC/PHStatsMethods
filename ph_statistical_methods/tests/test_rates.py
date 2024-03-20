# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 15:04:04 2024

@author: Jack.Burden_DHSC
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from rates import ph_rate

class TestRates:
    
    data = pd.read_excel('tests/test_data/testdata_Rate.xlsx', sheet_name = 'testdata_Rate').iloc[:,:-1]