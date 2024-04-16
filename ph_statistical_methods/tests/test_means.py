# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:22:46 2024

@author: Annabel.Westermann
"""
import pandas as pd

from pandas.testing import assert_frame_equal

from means import ph_mean


data = pd.read_excel('tests/test_data/testdata_Mean.xlsx', sheet_name = 'testdata_Mean')

results = pd.read_excel('tests/test_data/testdata_Mean.xlsx', sheet_name = 'testdata_Mean_results')


def test_default_group(data, results):
    df = ph_mean(data, 'values', 'area').drop(['Confidence'], axis=1)
    df2 = results.iloc[:2, :].drop(['lower_99_8_ci', 'upper_99_8_ci'], axis=1)
    assert_frame_equal(df, df2)