# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from .confidence_intervals import byars_lower, byars_upper
from .validation import metadata_cols, ci_col, validate_data, format_args, check_kwargs, group_args

def ph_ISRate(df, num_col, denom_col, ref_num_col, ref_denom_col, group_cols = None, 
                     metadata = True, confidence = 0.95, multiplier = 100000, **kwargs):
    
    """Calculates indirectly standardized rates with confidence limits using Byar's or exact CI method.

    Parameters
    ----------
    df
        DataFrame containing the data.
    num_col : str
        Field containing observed number of events.
    denom_col : str
        Field containing population at risk.
    ref_num_col : str
        Observed events in the reference population.
    ref_denom_col : str
        Population at risk in the reference population.
    group_cols : str | list
        Columns to group data by.
    metadata : bool 
        Include metadata columns.
    confidence : float | list 
        Confidence levels, default 0.95.
    multiplier : int 
        The multiplier for the rate calculation, default 100000.
        
        
    Other Parameters
    ----------------
    ref_df: 
        DataFrame of reference data to join.
    ref_join_left : str | list 
        A string or list of column name(s) in `df` to join on to.
    ref_join_right : str | list 
        A string or list of column name(s) in `ref_df` to join on to.
    obs_df 
        DataFrame of total observed events for each group.
    obs_join_left : str | list 
        A string or list of column name(s) in `df` to join on to.
    obs_join_right : str | list 
        A string or list of column name(s) in `obs_df` to join on to.
        
    Returns
    -------
    Pandas DataFrame
        Dataframe containing calculated IS Rates.
    
    Notes
    -----
    For numerators >= 10 Byar's method (1) is applied using the internal byars_lower and byars_upper functions. 
    For small numerators Byar's method is less accurate and so an exact method (2) based on the 
    Poisson distribution is used.

    References
    ----------
    (1) Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis
        of cohort studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    (2) Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.
    
    Examples
    --------
    from PHStatsMethods import ph_ISRate
    import pandas as pd
    import numpy as np

    df = pd.DataFrame({
        'indicatorid': np.repeat([1234, 5678, 91011, 121314], 19 * 2 * 5),
        'year': np.tile(np.repeat(np.arange(2006, 2011), 19 * 2), 4),
        'sex': np.tile(np.repeat(['Male', 'Female'], 19), 5 * 4),
        'ageband': np.tile(np.arange(0, 95, 5), 10 * 4),
        'obs': np.random.randint(0, 200, 19 * 2 * 5 * 4),
        'pop': np.random.randint(10000, 20000, 19 * 2 * 5 * 4)
    })

    # Create the reference dataframe refdf
    refdf = pd.DataFrame({
        'refcount': np.random.randint(0, 200, 19),
        'refpop': np.random.randint(10000, 20000, 19),
        'ageband': np.arange(0, 95, 5)
    })

   # Group by 'indicatorid', 'year', 'sex' and calculate ISRs
    result = ph_ISRate(
        df, 'obs', 'pop', 'refcount', 'refpop', 
        group_cols=['indicatorid', 'year', 'sex'],
        ref_df=refdf, ref_join_left='ageband', ref_join_right='ageband'
    )

    # Group by 'indicatorid', 'year', 'sex' and calculate ISRs without metadata fields
    result_no_metadata = ph_ISRate(
        df, 'obs', 'pop', 'refcount', 'refpop', 
        group_cols=['indicatorid', 'year', 'sex'],
        ref_df=refdf, ref_join_left='ageband', ref_join_right='ageband',
       metadata=False, confidence=0.998
    )


    # Group by 'indicatorid', 'year', 'sex' and calculate ISRs with multiple confidence intervals
    result_multiple_cis = ph_ISRate(
        df, 'obs', 'pop', 'refcount', 'refpop', 
        group_cols=['indicatorid', 'year', 'sex'],
        ref_df=refdf, ref_join_left='ageband', ref_join_right='ageband',
        confidence=[0.95, 0.998]
    )
    
    # Define the observed totals dataframe
    observed_totals = pd.DataFrame({
        'indicatorid': np.repeat([1234, 5678, 91011, 121314], 10),
        'year': np.tile(np.repeat(np.arange(2006, 2011), 2), 4),
        'sex': np.tile(np.repeat(['Male', 'Female'], 5), 4),
        'observed': np.random.randint(1500, 2500, 40)
    })
    
    # Merge observed totals with the main dataframe
    df_totals = df.drop(columns='obs').merge(observed_totals, on=['indicatorid', 'year', 'sex'])
    
    # Calculate ISRs with observed totals
    result_with_totals = ph_ISRate(
        df_totals, 'observed', 'pop', 'refcount', 'refpop', 
        group_cols=['indicatorid', 'year', 'sex'],
        ref_df=refdf, ref_join_left='ageband', ref_join_right='ageband'
    )
    
    
    """
    
    confidence, group_cols = format_args(confidence, group_cols)
    ref_df, ref_join_left, ref_join_right = check_kwargs(df, kwargs, 'ref', ref_num_col, ref_denom_col)
    obs_df, obs_join_left, obs_join_right = check_kwargs(df, kwargs, 'obs', num_col)
    df = validate_data(df, denom_col, group_cols, metadata, ref_df=ref_df)
    
    # Grouping by temporary column to reduce duplication in code
    df, group_cols = group_args(df, group_cols, True)

    if ref_df is not None:
        df = df.merge(ref_df, how='left', left_on=ref_join_left, right_on=ref_join_right).drop(ref_join_right, axis=1)
    
    df['exp_x'] = df[ref_num_col].fillna(0) / df[ref_denom_col] * df[denom_col].fillna(0)
    
    if obs_df is not None:
        df = df.groupby(group_cols).agg({'exp_x': lambda x: x.sum(skipna=False),
                                         ref_num_col: 'sum',
                                         ref_denom_col: lambda x: x.sum(skipna=False)}).reset_index()
        df = df.merge(obs_df, how = 'left', left_on = obs_join_left, right_on = obs_join_right)
    
    else:
        df = df.groupby(group_cols).agg({num_col: 'sum',
                                         'exp_x': lambda x: x.sum(skipna=False),
                                         ref_num_col: 'sum',
                                         ref_denom_col: lambda x: x.sum(skipna=False)}).reset_index()
        
    df['ref_rate'] = df[ref_num_col] / df[ref_denom_col] * multiplier
    
    # Tidy dataframe
    df = df.rename(columns={num_col: 'Observed', 'exp_x': 'Expected'}).\
        drop([ref_num_col, ref_denom_col], axis=1).reindex(columns=(group_cols + ['Observed', 'Expected', 'ref_rate']))
    
    df['Value'] = df['Observed'] / df['Expected'] * df['ref_rate']
    
    for c in confidence:
        df[ci_col(c, 'lower')] = df.apply(lambda x: byars_lower(x['Observed'], c), axis=1) / df['Expected'] * df['ref_rate']
        df[ci_col(c, 'upper')] = df.apply(lambda x: byars_upper(x['Observed'], c), axis=1) / df['Expected'] * df['ref_rate']

    if metadata:
        method = np.where(df['Observed'] < 10, 'Exact', 'Byars')
        df = metadata_cols(df, f'indirectly standardised rate per {multiplier}', confidence, method)
    
    if group_cols == ['ph_pkg_group']:
        df = df.drop(columns='ph_pkg_group') 

    return df
