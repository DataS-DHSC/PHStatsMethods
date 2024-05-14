# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:00:48 2024

@author: Annabel.Westermann
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from DSR import ph_dsr

data = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name='testdata_multiarea')
results = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name='testresults_DSR')\
    .drop('statistic', axis=1).astype({'Total Count':'float64'})  
ref_data = pd.read_excel('tests/test_data/testdata_DSR_ISR.xlsx', sheet_name='testdata_1976')

cols_95 = [0,1,2,3,4,5,8]

df = ph_dsr(data, 'count', 'pop', 'ageband', group_cols='area').drop(['Confidence', 'Statistic'], axis=1)
assert_frame_equal(df, results.iloc[4:7, cols_95].reset_index(drop=True))
