# -*- coding: utf-8 -*-

import pandas as pd

from validation import join_age_groups

def euro_standard_pop():
    
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34',
                  '35-39', '40-44', '45-49', '50-54', '55-59', '60-64',
                  '65-69', '70-74', '75-79', '80-84', '85-89', '90+']
    
    pops = [5000, 5500, 5500, 5500, 6000, 6000, 6500, 7000, 7000, 7000, 
            7000, 6500, 6000, 5500, 5000, 4000, 2500, 1500, 1000]
    
    data = pd.DataFrame({'age_group': age_groups,
                         'populations': pops})
    
    return data
