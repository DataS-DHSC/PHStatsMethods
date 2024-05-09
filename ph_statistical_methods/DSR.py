# -*- coding: utf-8 -*-

import pandas as pd

from utils import join_euro_standard_pops
from validation import format_args, validate_data, check_kwargs



df = pd.DataFrame({'year': [2017] * 19 + [2018]*19 + [2019]*19 + [2020]*19, 
                   'ageband': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
                               50, 55, 60, 65, 70, 75, 80, 85, 90] * 4,
                   'obs': [100, 300, 250, 400, 350] * 15 + [380],
                   'pop': [1000, 3000, 900, 1200, 2000] * 15 + [900]})

group_cols = 'year'
confidence = 0.95
denom_col = 'pop'
num_col = 'obs'

def ph_dsr(df, num_col, denom_col, ref_denom_col, group_cols = None, metadata = True, 
           confidence = 0.95, multiplier = 100000, euro_standard_pops = True, **kwargs)

df = df.copy().reset_index()

confidence, group_cols = format_args(confidence, group_cols)
ref_df, ref_join_left, ref_join_right = check_kwargs(df, kwargs, 'ref', ref_denom_col)
validate_data(df, num_col, group_cols, metadata, denom_col, ref_df = ref_df)

# Join reference data
if euro_standard_pops:
    df = join_euro_standard_pops(df, ref_denom_col, group_cols)
    ref_denom_col = 'euro_standard_pops'
    
elif ref_df is not None:
    df = df.merge(ref_df, on = 'left', left_on = ref_join_left, right_on = ref_join_right)
    
df['wt_rate'] = df[num_col].fillna(0) * df[ref_denom_col] / df[denom_col]
df['sq_rate'] = df[num_col].fillna(0) * (df[ref_denom_col] / df[denom_col]**2)

dsr = df.groupby(group_cols).agg({num_col: 'sum', 
                                  denom_col: lambda x: x.sum(skipna=False), 
                                  'wt_rate': lambda x: x.sum(skipna=False),
                                  ref_denom_col: lambda x: x.sum(skipna=False), 
                                  'sq_rate': lambda x: x.sum(skipna=False)})

dsr['Value'] = dsr['wt_rate'] / dsr[ref_denom_col] * multiplier
dsr['vardsr'] = 1 / dsr[ref_denom_col]**2 * dsr['sq_rate']
