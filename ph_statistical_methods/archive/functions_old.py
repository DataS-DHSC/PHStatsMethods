"""
functions.py
==================================
Calculations for rates, means, and proportions used in public health calculations. These calculations can be applied to
data frames,

Applying directly standardised ratios, standardised mortality ratios and indirectly standardised ratios to data frames.
"""


import warnings
import pandas as pd
from scipy.stats import t, sem
from statistics import mean
from .methods import byars, exact, wilson, european_standard_pop, phe_dsr, eng_standard_deaths, eng_standard_pop, \
    phe_smr, phe_isr
from .validation import validate_data


def phe_rate(numerator, denominator=None, multiplier=None, metadata=True, alpha=0.05):
    """
    Calculates rates with confidence limits using Byar's [1] or exact [2] CI method.

    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    [2] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param numerator: Numerator Value as float
    :param denominator: Denominator Value as float
    :param multiplier: number to multiply the calculation output as float
    :param metadata: Boolean. When true returns a column called metadata containing a dict of metadata. Default True
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: Tuple of rate/numerator, lower confidence interval, and upper confidence intervals as float
    """
    validate_data(numerator, denominator, multiplier, metadata, alpha)
    if numerator < 10:
        cis = exact(numerator, alpha=alpha)
        method = 'exact'
    else:
        cis = byars(numerator, alpha=alpha)
        method = 'Byars'
    if denominator and not multiplier or multiplier and not denominator:
        warnings.warn('If using a denominator, a multiplier must also be specified')
    if denominator and multiplier:
        value = numerator / denominator * multiplier
        lower_ci = cis[0] / denominator * multiplier
        upper_ci = cis[1] / denominator * multiplier
        return value, lower_ci, upper_ci

    if metadata:
        if multiplier:
            multiplier_text = 'Rate per' + str(multiplier)
        else:
            multiplier_text = 'Rate'
        metadata_to_return = {
            'confidence': str((1 - alpha) * 100) + '%',
            'statistic': multiplier_text,
            'method': method
        }
        return numerator, cis[0], cis[1], metadata_to_return
    return numerator, cis[0], cis[1]


def phe_mean(data, metadata=True, alpha=0.05):
    """
    Calculates means with confidence limits using Student's t-distribution method.

    :param data: A list or array of floats or ints
    :param metadata: Boolean. When true returns a column called metadata containing a dict of metadata. Default True
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: A tuple of mean, lower confidence interval, and upper confidence interval calculated using student's t
             method as float
    """
    validate_data(data, metadata=metadata, alpha=alpha)
    data_mean = mean(data)
    cis = t.interval(alpha, len(data) - 1, loc=data_mean, scale=sem(data))

    if metadata:
        metadata_to_return = {
            'confidence': str((1 - alpha) * 100) + '%',
            'statistic': 'Mean',
            'method': 'Student\'s t-distribution'
        }
        return data_mean, cis[0], cis[1], metadata_to_return
    return data_mean, cis[0], cis[1]


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
    validate_data(numerator, denominator, multiplier, metadata, alpha)

    cis = wilson(numerator, denominator, alpha=alpha, rate=multiplier)
    if metadata:
        metadata_to_return = {
            'confidence': str((1 - alpha) * 100) + '%',
            'statistic': 'Proportion per ' + str(multiplier),
            'method': 'Wilson'
        }
        return numerator / denominator * multiplier, cis[0], cis[1], metadata_to_return
    return numerator / denominator * multiplier, cis[0], cis[1]


def apply_proportion_to_dataframe(df, numerator_column, denominator_column, metadata=True, alpha=0.05, multiplier=1):
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
            row[numerator_column],
            row[denominator_column],
            metadata=metadata,
            multiplier=multiplier,
            alpha=alpha),
                                                                                         axis=1))

        df = pd.concat([df.drop(['metadata'], axis=1), df['metadata'].apply(pd.Series)], axis=1)
        return df
    df['proportion'], df['lower_ci'], df['upper_ci'] = zip(*df.apply(lambda row: phe_proportion(
        row[numerator_column],
        row[denominator_column],
        metadata=metadata,
        multiplier=multiplier,
        alpha=alpha),
                                                                     axis=1))
    return df


def apply_rate_to_dataframe(df, numerator_column, denominator_column=None, metadata=True, alpha=0.05, multiplier=None):
    """
    Apply the function phe_rate to an entire data frame for a given numerator and denominator column.

    phe_rate calculates rates with confidence limits using Byar's [1] or exact [2] CI method.

    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    [2] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param df: A complete pandas data frame with no missing values in the numerator and denominator columns
    :param numerator_column: Name of the column that contains the numerator values
    :param denominator_column: Name of the column that contains the denominator values
    :param metadata: Boolean. When true returns a column called metadata containing a dict of metadata. Default True
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :param multiplier: Number to multiply the result to get a percentage or proportion. Default None
    :return: A pandas dataframe with extra columns containing rate values and confidence intervals and [optional]
    metadata
    """

    if metadata:
        df['rate'], df['lower_ci'], df['upper_ci'], df['metadata'] = zip(*df.apply(lambda row: phe_rate(
                                                                                          row[numerator_column],
                                                                                          row[denominator_column],
                                                                                          metadata=metadata,
                                                                                          multiplier=multiplier,
                                                                                          alpha=alpha),
                                                                         axis=1))
        df = pd.concat([df.drop(['metadata'], axis=1), df['metadata'].apply(pd.Series)], axis=1)
        return df
    df['rate'], df['lower_ci'], df['upper_ci'] = zip(*df.apply(lambda row: phe_rate(row[numerator_column],
                                                                                    row[denominator_column],
                                                                                    multiplier=multiplier,
                                                                                    alpha=alpha),
                                                               axis=1))
    return df


def apply_mean_to_dataframe(df, columns_to_calculate, metadata=True, alpha=0.05):
    """
    Apply the function phe_mean to an entire data frame for a given numerator and denominator column.

    phe_mean calculates means with confidence limits using Student's t-distribution method.

    :param df: A complete pandas data frame with no missing values in the columns to calculate
    :param columns_to_calculate: A list of column names to calculate
    :param metadata: Boolean. When true returns a column called metadata containing a dict of metadata. Default True
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: The original data frame with columns for mean, confidence interval and [optional] metadata added
    """
    if metadata:
        df['mean'], df['lower_ci'], df['upper_ci'], df['metadata'] = zip(*df.apply(lambda row: phe_mean(
                                                                                          row[columns_to_calculate],
                                                                                          metadata=metadata,
                                                                                          alpha=alpha),
                                                                                   axis=1))
        df = pd.concat([df.drop(['metadata'], axis=1), df['metadata'].apply(pd.Series)], axis=1)
        return df
    df['mean'], df['lower_ci'], df['upper_ci'] = zip(*df.apply(lambda row: phe_mean(row[columns_to_calculate],
                                                                                    alpha=alpha),
                                                               axis=1))
    return df


def get_dsr_from_dataframe(df, count_column, population_column, multiplier=100000, area_column=False,
                           ref_pop_array=european_standard_pop, metadata=True, alpha=0.05):
    """
    Creates a data frame with a directly standardised ratios from a data frame of values.

    Calculates directly standardised rates with confidence limits using Byar's method [1] with Dobson method adjustment
    [2].

    User MUST ensure that x, n and stdpop vectors are all ordered by the same standardisation category values as records
    will be matched by position. For total counts >= 10 Byar's method [1] is applied using the byars_lower and
    byars_upper functions.  When the total count is < 10 DSRs are not reliable and will therefore not be calculated.

    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    [2] Dobson A et al. Confidence intervals for weighted sums of Poisson parameters. Stat Med 1991;10:457-62.

    :param df: A pandas data frame of values that can be used to calculate directly standardised ratios
    :param area_column: Column with area codes or references
    :param count_column: Column with area counts by age bracket
    :param population_column: Column with area population by age bracket
    :param multiplier: Number to multiply the result to get the standardised rate. Default 100000
    :param ref_pop_array: The model population array. Default to European Standard Population
    :param metadata: Boolean. When true returns a column called metadata containing a dict of metadata. Default True
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: A new data frame with DSR values, confidence intervals, [optional] metadata, for areas passed in
    """
    dsr_df = pd.DataFrame()
    if area_column:
        areas = df[area_column].unique()
        for area in areas:
            area_df = df[df[area_column] == area]
            if area_df.shape[1] != ref_pop_array:
                raise ValueError('Data for {} is not the same length of the population reference data'.format(area))
            if metadata:
                columns = ['area', 'value', 'lower_ci', 'upper_ci', 'confidence', 'statistic', 'method']
                dsr, upper_ci, lower_ci, metadata = phe_dsr(area_df[count_column], area_df[population_column],
                                                            multiplier=multiplier, ref_pop_array=ref_pop_array,
                                                            metadata=True, alpha=alpha)
                confidence, statistic, method = zip(*metadata)
                area_info = pd.DataFrame([area, dsr, lower_ci, upper_ci, confidence, statistic, method],
                                         columns=columns)
            else:
                columns = ['area', 'value', 'lower_ci', 'upper_ci']
                dsr, upper_ci, lower_ci = phe_dsr(area_df[count_column], area_df[population_column],
                                                  multiplier=multiplier, ref_pop_array=ref_pop_array, metadata=False,
                                                  alpha=alpha)
                area_info = pd.DataFrame([area, dsr, lower_ci, upper_ci], columns=columns)
            dsr_df = dsr_df.append(area_info)
    else:
        if metadata:
            columns = ['value', 'lower_ci', 'upper_ci', 'confidence', 'statistic', 'method']
            dsr, upper_ci, lower_ci, metadata = phe_dsr(df[count_column], df[population_column],
                                                        multiplier=multiplier, ref_pop_array=ref_pop_array,
                                                        metadata=metadata, alpha=alpha)
            confidence, statistic, method = zip(*metadata)
            dsr_df = pd.DataFrame([dsr, lower_ci, upper_ci, confidence, statistic, method], columns=columns)
        else:
            columns = ['value', 'lower_ci', 'upper_ci']
            dsr, upper_ci, lower_ci = phe_dsr(df[count_column], df[population_column], multiplier=multiplier,
                                              ref_pop_array=ref_pop_array, metadata=False, alpha=alpha)
            dsr_df = pd.DataFrame([dsr, lower_ci, upper_ci], columns=columns)
    return dsr_df


def get_smr_from_dataframe(df, obs_death_column, population_column, multiplier=100000, area_column=False,
                           ref_pop_array=eng_standard_pop , ref_deaths_array=eng_standard_deaths, metadata=True,
                           alpha=0.05):
    """
    This function applies the phe_smr function to a data frame object with either a single area's data or to multiple
    areas. For multiple areas the optional area_column parameter should be completed with a unique identifier for each
    area. All areas should have the same length as the reference population and reference deaths arrays.

    phe_smr calculates standard mortality ratios (or indirectly standardised ratios) with confidence limits using
    Byar's [1] or exact [2] CI method.

    User MUST ensure that x, n, x_ref and n_ref vectors are all ordered by the same standardisation category values as
    records will be matched by position. For numerators >= 10 Byar's method [1] is applied using the byars_lower and
    byars_upper functions. For small numerators Byar's method is less accurate and so an exact method [2] based on the
    Poisson distribution is used.

    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    [2] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param df: Data frame object with area data
    :param obs_death_column: Name of the column that contains the area's observed deaths data
    :param population_column: Name of the column that contains the area's population data
    :param multiplier: Number to multiply the result to get the standardised rate. Default 100000
    :param area_column: Unique identifier for each area if multiple areas are required
    :param ref_pop_array: Series or array or list of reference deaths to standardise to
    :param ref_deaths_array: Series or array or list of reference populations to standardise to
    :param metadata: Metadata used in this calculation; confidence, statistic & method. Default to True
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :return: A data frame of standardised mortality ratios for each area with confidence intervals and [optional]
    metadata
    """
    smr_df = pd.DataFrame()
    if area_column:
        areas = df[area_column].unique()
        for area in areas:
            area_df = df[df[area_column] == area]
            if area_df.shape[1] != ref_pop_array or area_df.shape[1] != ref_deaths_array:
                raise ValueError('Data for {} is not the same length of the reference data'.format(area))
            if metadata:
                columns = ['area', 'value', 'lower_ci', 'upper_ci', 'confidence', 'statistic', 'method']
                smr, upper_ci, lower_ci, metadata = phe_smr(area_df[obs_death_column], area_df[population_column],
                                                            reference_deaths=ref_deaths_array,
                                                            reference_population=ref_pop_array, multiplier=multiplier,
                                                            metadata=metadata, alpha=alpha)
                confidence, statistic, method = zip(*metadata)
                area_info = pd.DataFrame([area, smr, lower_ci, upper_ci, confidence, statistic, method],
                                         columns=columns)
            else:
                columns = ['area', 'value', 'lower_ci', 'upper_ci']
                smr, upper_ci, lower_ci = phe_smr(area_df[obs_death_column], area_df[population_column],
                                                  reference_deaths=ref_deaths_array, reference_population=ref_pop_array,
                                                  multiplier=multiplier, metadata=metadata, alpha=alpha)
                area_info = pd.DataFrame([area, smr, upper_ci, lower_ci], columns=columns)
            smr_df = smr_df.append(area_info)
    else:
        if metadata:
            columns = ['value', 'lower_ci', 'upper_ci', 'confidence', 'statistic', 'method']
            smr, upper_ci, lower_ci, metadata = phe_smr(df[obs_death_column], df[population_column],
                                                        reference_deaths=ref_deaths_array,
                                                        reference_population=ref_pop_array, multiplier=multiplier,
                                                        metadata=metadata, alpha=alpha)
            confidence, statistic, method = zip(*metadata)
            smr_df = pd.DataFrame([smr, lower_ci, upper_ci, confidence, statistic, method], columns=columns)
        else:
            columns = ['value', 'lower_ci', 'upper_ci']
            smr, upper_ci, lower_ci = phe_smr(df[obs_death_column], df[population_column],
                                              reference_deaths=ref_deaths_array, reference_population=ref_pop_array,
                                              multiplier=multiplier, metadata=metadata, alpha=alpha)
            smr_df = pd.DataFrame([smr, lower_ci, upper_ci], columns=columns)
    return smr_df


def get_isr_from_dataframe(df, obs_column, population_column, reference_obs_array, reference_pop_array, multiplier=100000,
                           metadata=True, area_column=None, alpha=0.05):
    """
    This function applies the phe_isr function to a data frame object with either a single area's data or to multiple
    areas. For multiple areas the optional area_column parameter should be completed with a unique identifier for each
    area. All areas should have the same length as the reference population and reference observation arrays.

    phe_isr calculates indirectly standardised rates with confidence limits using Byar's [1] or exact [2] CI method.

    User MUST ensure that obs_array, population_array, reference_obs_array and reference_pop_array vectors are all
    ordered by the same standardisation category values as records will be matched by position. For numerators >= 10
    Byar's method [1] is applied using the byars_lower and byars_upper functions. For small numerators Byar's method is
    less accurate and so an exact method [2] based on the Poisson distribution is used.

    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    [2] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param df: Data frame object with area data
    :param obs_column: Name of the column that contains the area's observed events data
    :param population_column: Name of the column that contains the area's population data
    :param reference_obs_array: Series or array or list of reference events to standardise to
    :param reference_pop_array: Series or array or list of reference populations to standardise to
    :param multiplier: Number to multiply the result to get the standardised rate. Default 100000
    :param metadata: Metadata used in this calculation; confidence, statistic & method. Default to True
    :param area_column: Unique identifier for each area if multiple areas are required
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :return:A data frame of indirectly standardised ratios for each area with confidence intervals and [optional]
    metadata
    """
    isr_df = pd.DataFrame()
    if area_column:
        areas = df[area_column].unique()
        for area in areas:
            area_df = df[df[area_column] == area]
            if area_df.shape[1] != reference_pop_array or area_df.shape[1] != reference_obs_array:
                raise ValueError('Data for {} is not the same length of the reference data'.format(area))
            if metadata:
                columns = ['area', 'value', 'lower_ci', 'upper_ci', 'confidence', 'statistic', 'method']
                isr, upper_ci, lower_ci, metadata = phe_isr(area_df[obs_column], area_df[population_column],
                                                            reference_events=reference_obs_array,
                                                            reference_population=reference_pop_array,
                                                            multiplier=multiplier, metadata=metadata, alpha=alpha)
                confidence, statistic, method = zip(*metadata)
                area_info = pd.DataFrame([area, isr, lower_ci, upper_ci, confidence, statistic, method],
                                         columns=columns)
            else:
                columns = ['area', 'value', 'lower_ci', 'upper_ci']
                isr, upper_ci, lower_ci = phe_isr(area_df[obs_column], area_df[population_column],
                                                  reference_events=reference_obs_array,
                                                  reference_population=reference_pop_array,
                                                  multiplier=multiplier, metadata=metadata, alpha=alpha)
                area_info = pd.DataFrame([area, isr, upper_ci, lower_ci], columns=columns)
            isr_df = isr_df.append(area_info)
    else:
        if metadata:
            columns = ['value', 'lower_ci', 'upper_ci', 'confidence', 'statistic', 'method']
            isr, upper_ci, lower_ci, metadata = phe_isr(df[obs_column], df[population_column],
                                                        reference_events=reference_obs_array,
                                                        reference_population=reference_pop_array,
                                                        multiplier=multiplier, metadata=metadata, alpha=alpha)
            confidence, statistic, method = zip(*metadata)
            isr_df = pd.DataFrame([isr, lower_ci, upper_ci, confidence, statistic, method], columns=columns)
        else:
            columns = ['value', 'lower_ci', 'upper_ci']
            isr, upper_ci, lower_ci = phe_isr(df[obs_column], df[population_column],
                                              reference_events=reference_obs_array,
                                              reference_population=reference_pop_array,
                                              multiplier=multiplier, metadata=metadata, alpha=alpha)
            isr_df = pd.DataFrame([isr, lower_ci, upper_ci], columns=columns)

    return isr_df
