# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 16:52:40 2024

@author: Annabel.Westermann
"""

import pandas as pd

from ph_statistical_methods.confidence_intervals import wilson, wilson_lower, wilson_upper


df = pd.read_excel('ph_statistical_methods/unit_tests/test_data/testdata_Proportion.xlsx')

df = pd.DataFrame({'area': ['Area1', 'Area2', 'Area3','Area4']*3,
                  'num': [None, 82, 9, 48, 6500, 8200, 10000, 10000, 8, 7, 750, 900],
                  'den': [100, 10000, 10000, 10000] * 3})


def ph_proportion_calc(numerator, denominator, multiplier = 1, confidence = None):
    
    proportion = (numerator / denominator) * multiplier
    
    if confidence is not None:
        prop_dict = {}
        prop_dict['Proportion'] = proportion
        
        # handle parameter if passed as float
        # TODO: make this part of the formatting checks! 
        if type(confidence) == float:
            confidence = [confidence]
        
        # get confidence interval for all given confidence intervals
        for c in confidence:
            prop_dict[f'CI_{c}'] = wilson(numerator, denominator, rate = multiplier, alpha = 1-c)
        
        # set return object to dictionary
        proportion = prop_dict
        
    return proportion
            
            
        
def ph_proportion(df, numerator_col, denominator_col, metadata = True, 
                  confidence = [0.95, 0.998], multiplier = 1):
    
    df['Value'] = df.apply(lambda x: ph_proportion_calc(x[numerator_col], x[denominator_col], multiplier),
                           axis=1)

    if confidence is not None:
        if type(confidence) == float:
            confidence = [confidence]
    
        for c in confidence:
            c_text = '0_' + str(c)[2:]
            df[f'lower_{c_text}_CI'] = df.apply(lambda x: wilson_lower(x[numerator_col], x[denominator_col], multiplier, 1-c),
                                                axis=1)
            df[f'upper_{c_text}_CI'] = df.apply(lambda x: wilson_upper(x[numerator_col], x[denominator_col], multiplier, 1-c),
                                                axis=1)
        
    return df
    



def phe_proportion(numerator, denominator, metadata=True, alpha=0.05, multiplier=1):
    """
    Calculates proportions with confidence limits using Wilson Score method [1, 2].

    [1] Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg
    209 to 212.
    [2] Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence
    (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.

    :param numerator: Numerator as int or float
    :param denominator: Denominator as int or float
    :param metadata: Boolean. When true returns a column called metadata containing a dict of metadata. Default True
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :param multiplier: Number to multiply the result to get a percentage or proportion. Default 1
    :return: A tuple of proportion or percentage, lower confidence interval, and upper confidence interval calculated
             using Wilson's method
    """
    #validate_data(numerator, denominator, multiplier, metadata, alpha)

    cis = wilson(numerator, denominator, alpha=alpha, rate=multiplier)
    if metadata:
        metadata_to_return = {
            'confidence': str((1 - alpha) * 100) + '%',
            'statistic': 'Proportion per ' + str(multiplier),
            'method': 'Wilson'
        }
        return numerator / denominator * multiplier, cis[0], cis[1], metadata_to_return
    return numerator / denominator * multiplier, cis[0], cis[1]


def apply_proportion_to_dataframe(df, numerator_col, denominator_col, metadata=True, alpha=0.05, multiplier=1):
    """
    Apply the function phe_proportion to an entire data frame for a given numerator and denominator column.

    phe_proportions calculates proportions with confidence limits using Wilson Score method [1, 2].

    [1] Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg
    209 to 212.
    [2] Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence
    (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.

    :param df: A complete pandas data frame with no missing values in the numerator and denominator columns
    :param numerator_column: Name of the column that contains the numerator values
    :param denominator_column: Name of the column that contains the denominator values
    :param metadata: Boolean. When true returns a column called metadata containing a dict of metadata. Default True
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :param multiplier: Number to multiply the result to get a percentage or proportion. Default 1
    :return: A pandas dataframe with extra columns containing proportion values and confidence intervals and [optional]
    metadata
    """


    if metadata:
        df['proportion'], df['lower_ci'], df['upper_ci'], df['metadata'] = zip(*df.apply(lambda row: phe_proportion(
            row[numerator_col],
            row[denominator_col],
            metadata=metadata,
            multiplier=multiplier,
            alpha=alpha),
                                                                                         axis=1))

        df = pd.concat([df.drop(['metadata'], axis=1), df['metadata'].apply(pd.Series)], axis=1)
        return df
    df['proportion'], df['lower_ci'], df['upper_ci'] = zip(*df.apply(lambda row: phe_proportion(
        row[numerator_col],
        row[denominator_col],
        metadata=metadata,
        multiplier=multiplier,
        alpha=alpha),
                                                                     axis=1))
    return df