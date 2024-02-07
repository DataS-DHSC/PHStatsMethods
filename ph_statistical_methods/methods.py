"""
methods.py
==================================
Functions to calculate and return confidence intervals and methods used in public health calculations.
"""


import warnings
import numpy as np
import pandas as pd
from math import sqrt
from scipy.special import ndtri
from scipy.stats import chi2
from .validation import validate_arrays, check_dataframe_for_errors, validate_data


# The European Standard Population for use in DSR calculation
european_standard_pop = np.array([5000, 5500, 5500, 5500, 6000, 6000, 6500, 7000, 7000, 7000, 7000, 6500, 6000, 5500,
                                  5000, 4000, 2500, 1500, 1000])


def get_calc_variables(a):
    """
    Creates the cumulative normal distribution and z score for a given alpha

    :param a: alpha
    :return: cumulative normal distribution, z score
    """
    norm_cum_dist = ndtri((100 + (100 - (100 * a))) / 200)
    z = ndtri(1 - a / 2)
    return norm_cum_dist, z


def wilson_lower(count, denominator, rate=100, alpha=0.05):
    """
    Calculates the lower CI using Wilson Score method [1, 2]. Takes in value, numerator, denominator, rate (default 100), and alpha
     (default 0.05)
    [1] Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg
    209 to 212. \cr
    [2] Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence
     (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.
    :param count: Numerator
    :param denominator: Denominator
    :param rate: Rate (default 100 for ratios)
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: Lower confidence interval as float
    """
    norm_cum_dist, z = get_calc_variables(alpha)
    lower_ci = ((2 * count + norm_cum_dist ** 2 - norm_cum_dist * sqrt(norm_cum_dist ** 2 + 4 * count * ((rate -
                (count / denominator * rate)) / rate))) / 2 / (denominator + norm_cum_dist ** 2)) * rate
    return lower_ci


def wilson_upper(count, denominator, rate=100, alpha=0.05):
    """
    Calculates the upper CI using Wilson Score method [1, 2]. Takes in value, numerator, denominator, rate (default 100), and alpha
     (default 0.05)
    [1] Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg
    209 to 212. \cr
    [2] Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence
     (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.
    :param count: Numerator
    :param denominator: Denominator
    :param rate: Rate (default 100 for ratios)
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: Upper confidence interval as float
    """
    norm_cum_dist, z = get_calc_variables(alpha)
    upper_ci = (2 * count + norm_cum_dist ** 2 + norm_cum_dist * sqrt(norm_cum_dist ** 2 + 4 * count * ((rate - (count /
                denominator * rate)) / rate))) / 2 / (denominator + norm_cum_dist ** 2) * rate
    return upper_ci


def wilson(count, denominator, rate=100, alpha=0.05):
    """
    Calculates the CI using Wilson Score method [1, 2]. Takes in value, numerator, denominator, rate (default 100), and alpha
     (default 0.05)
    [1] Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc; 1927; 22. Pg
    209 to 212. \cr
    [2] Newcombe RG, Altman DG. Proportions and their differences. In Altman DG et al. (eds). Statistics with confidence
     (2nd edn). London: BMJ Books; 2000. Pg 46 to 48.
    :param count: Numerator
    :param denominator: Denominator
    :param rate: Rate (default 100 for ratios)
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: Lower and Upper confidence intervals as a tuple
    """
    return wilson_lower(count, denominator, rate, alpha), wilson_upper(count, denominator, rate, alpha)


def exact_upper(value, alpha=0.05):
    """
    Calculates upper confidence interval using the exact method[1].
    [1] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param value: Value to calculate upper confidence interval
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: Upper confidence interval as a float
    """
    o = 2 * value + 2
    upper_ci = chi2.ppf(1 - (alpha / 2), o) / 2
    return upper_ci


def exact_lower(value, alpha=0.05):
    """
    Calculates lower confidence interval using the exact method[1].
    [1] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param value: Value to calculate lower confidence interval
    :param alpha: Alpha - default 0.05 for 95% confidence interval
    :return: Lower confidence interval as a float
    """
    o = 2 * value
    lower_ci = chi2.ppf(alpha / 2, o) / 2
    return lower_ci


def exact(value, alpha=0.05):
    """
    Calculates confidence intervals using the exact method[1].
    [1] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param value: Value to calculate confidence intervals
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :return: Lower and Upper confidence intervals as a tuple
    """
    return exact_lower(value, alpha=alpha), exact_upper(value, alpha=alpha)


def byars_lower(value, alpha=0.05):
    """
    Calculates lower confidence interval using Byar's method[1].
    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.

    :param value: Value to calculate lower confidence interval
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :return: Lower confidence interval as a float
    """
    calc_vars = get_calc_variables(alpha)
    if value < 10:
        return exact_lower(value, alpha)
    else:
        return value * (1 - (1 / (9 * value)) - calc_vars[1] / (3 * sqrt(value))) ** 3


# calculates the upper CI using Byar's method without using denominator. Takes in count and alpha (default 0.05)
def byars_upper(value, alpha=0.05):
    """
    Calculates upper confidence interval using Byar's method[1].
    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.

    :param value: Value to calculate upper confidence interval
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :return: Upper confidence interval as a float
    """
    calc_vars = get_calc_variables(alpha)
    if value < 10:
        return exact_upper(value, alpha)
    else:
        return (value + 1) * (1 - (1 / (9 * value + 1)) + calc_vars[1] / (3 * sqrt(value + 1))) ** 3


# calculates the upper and lower CIs using Byar's method without denominator and returns in a tuple
def byars(value, alpha=0.05, denominator=None, rate=None, exact_method_for_low_numbers=True):
    """
    Calculates confidence intervals using Byar's method[1].
    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.

    :param value: Value to calculate confidence intervals, must be over 9 to calculate Byar's, else exact method is used
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :param denominator: (Optional) Denominator to calculate Byar's on a rate
    :param rate: (Optional) Rate
    :param exact_method_for_low_numbers: Boolean instruction as to whether to use exact method for low numbers. Default
                                         True
    :return: Either exact method or Byar's method confidence intervals in a tuple
    """
    if denominator and not rate or rate and not denominator:
        raise ValueError('To use a denominator, you must also provide a rate')
    if value < 10 and exact_method_for_low_numbers:
        warnings.warn('As the sample is small, the exact method is used to calculate confidence intervals')
        upper_exact = exact_upper(value, alpha)
        lower_exact = exact_lower(value, alpha)
        if denominator and rate:
            return (lower_exact / denominator) * rate, (upper_exact / denominator) * rate
        else:
            return lower_exact, upper_exact
    elif value < 10:
        warnings.warn('As the sample is small and exact method not used, Byar\'s cannot be accurately calculated. '
                      'Not-a-number will be returned')
        return np.nan, np.nan
    if denominator and rate:
        return (byars_lower(value, alpha) / denominator) * rate, (byars_upper(value, alpha) / denominator) * rate
    else:
        return byars_lower(value, alpha), byars_upper(value, alpha)


def phe_dsr(obs_array, pop_array, multiplier=100000, ref_pop_array=european_standard_pop, metadata=True, alpha=0.05):
    """
    Calculates directly standardised rates with confidence limits using Byar's method [1] with Dobson method adjustment
    [2].

    User MUST ensure that x, n and stdpop vectors are all ordered by the same standardisation category values as records
    will be matched by position. For total counts >= 10 Byar's method [1] is applied using the byars_lower and
    byars_upper functions.  When the total count is < 10 DSRs are not reliable and will therefore not be calculated.

    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    [2] Dobson A et al. Confidence intervals for weighted sums of Poisson parameters. Stat Med 1991;10:457-62.


    :param obs_array: An array or list of observed values
    :param pop_array: An array or list of population values
    :param multiplier: Multiplier to normalise output (default to 100000)
    :param ref_pop_array: The model population array (default to European Standard Population)
    :param metadata: A dictionary of metadata used in this calculation; confidence, statistic & method. Default to True
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :return: The directly standardised rate, lower, and upper confidence intervals as a tuple
    """
    validate_data(multiplier=multiplier, metadata=metadata, alpha=alpha)
    validate_arrays([obs_array, pop_array, ref_pop_array], obs_array=obs_array, pop_array=pop_array)

    # creates a dataframe with the arrays
    frame = pd.DataFrame(np.column_stack([obs_array, pop_array, ref_pop_array]), columns=['obs', 'pop', 'stdpop'])
    check_dataframe_for_errors(frame)
    # calculates WiOi/Ni
    frame['rate'] = frame['stdpop'] / frame['pop'] * frame['obs']

    # calculates Wi2Oi/Ni2
    frame['rate_multiplier'] = (frame['stdpop'] / frame['pop']) ** 2 * frame['obs']
    dsr_out = frame['rate'].sum() / frame['stdpop'].sum() * multiplier
    if dsr_out < 10:
        warnings.warn('A DSR could not be accurately calculated as sum of observed values is below 10')
        return np.nan, np.nan, np.nan
    obs_total = frame['obs'].sum()

    # get Byars CIs for observed values
    obs_conf = byars(obs_total, alpha=alpha)

    # calculate the variance in DSR values
    var_dsr = frame['rate_multiplier'].sum() / frame['stdpop'].sum() ** 2
    # calculate the CIs for DSR using Dobson method
    dsr_conf_lower = (dsr_out / multiplier) + sqrt(var_dsr / obs_total) * (obs_conf[0] - obs_total)
    dsr_conf_upper = (dsr_out / multiplier) + sqrt(var_dsr / obs_total) * (obs_conf[1] - obs_total)

    if metadata:
        metadata_to_return = {
            'confidence': str((1 - alpha) * 100) + '%',
            'statistic': 'DSR per ' + str(multiplier),
            'method': 'Dobson'
        }
        return dsr_out, dsr_conf_lower * multiplier, dsr_conf_upper * multiplier, metadata_to_return

    return dsr_out, dsr_conf_lower * multiplier, dsr_conf_upper * multiplier


def phe_isr(local_observed_events, local_population, reference_events, reference_population, multiplier=100000,
            metadata=True, alpha=0.05):
    """
    Calculates indirectly standardised rates with confidence limits using Byar's [1] or exact [2] CI method.

    User MUST ensure that obs_array, population_array, reference_obs_array and reference_pop_array vectors are all
    ordered by the same standardisation category values as records will be matched by position. For numerators >= 10
    Byar's method [1] is applied using the byars_lower and byars_upper functions. For small numerators Byar's method is
    less accurate and so an exact method [2] based on the Poisson distribution is used.

    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    [2] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param local_observed_events: Series or array or list of observed events within an area
    :param local_population: Series or array or list of the population within which the events occurred
    :param reference_events: Series or array or list of reference events to standardise to
    :param reference_population: Series or array or list of reference populations to standardise to
    :param multiplier: Multiplier to normalise output (default to 100000)
    :param metadata: A dictionary of metadata used in this calculation; confidence, statistic & method. Default to True
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :return: The indirectly standardised rate, lower, and upper confidence intervals as a tuple
    """
    validate_data(multiplier=multiplier, metadata=metadata, alpha=alpha)
    validate_arrays([local_observed_events, local_population, reference_events, reference_population],
                    obs_array=local_observed_events, pop_array=local_population)

    frame = pd.DataFrame(np.column_stack([local_observed_events, local_population, reference_events,
                                          reference_population]), columns=['obs', 'pop', 'ref_events', 'ref_pop'])
    check_dataframe_for_errors(frame)
    frame['ref_rates'] = frame['ref_events'] / frame['ref_pop']
    frame['expected_events'] = frame['ref_rates'] * frame['pop']
    expected_count = frame['expected_events'].sum()
    sum_events = frame['obs'].sum()
    if multiplier == 100 or multiplier == 1:
        isr_out = (sum_events / expected_count) * multiplier
    else:
        reference_crude_rate = (frame['ref_events'].sum() / frame['ref_rates'].sum()) * multiplier
        isr_out = (sum_events / expected_count) * reference_crude_rate

    if sum_events < 10:
        isr_confs = exact(sum_events, alpha=alpha)
    else:
        isr_confs = byars(sum_events, alpha=alpha)

    if metadata:
        metadata_to_return = {
            'confidence': str((1 - alpha) * 100) + '%',
            'statistic': 'ISR per ' + str(multiplier),
            'method': 'Byars'
        }
        return isr_out, (isr_confs[0] / expected_count) * multiplier, (isr_confs[1] / expected_count) * multiplier, \
               metadata_to_return
    return isr_out, (isr_confs[0] / expected_count) * multiplier, (isr_confs[1] / expected_count) * multiplier


eng_standard_pop = np.array([297256, 1247768, 1663285, 1666353, 1568759, 1525390, 1789723, 2047096, 2098035, 1822329,
                            1669145, 1813517, 1453409, 1298083, 1188619, 1131035, 1042657, 710306])

eng_standard_deaths = np.array([1449, 272, 198, 171, 386, 472, 632, 1033, 1629, 2229, 3300, 5684, 7352, 10256, 15230,
                                25409, 39762, 49274])


def phe_smr(observed_deaths, population, reference_deaths=eng_standard_deaths, reference_population=eng_standard_pop,
            multiplier=100, metadata=True, alpha=0.05):
    """
    Calculates standard mortality ratios (or indirectly standardised ratios) with confidence limits using Byar's [1] or
    exact [2] CI method.

    User MUST ensure that x, n, x_ref and n_ref vectors are all ordered by the same standardisation category values as
    records will be matched by position. For numerators >= 10 Byar's method [1] is applied using the byars_lower and
    byars_upper functions. For small numerators Byar's method is less accurate and so an exact method [2] based on the
    Poisson distribution is used.

    [1] Breslow NE, Day NE. Statistical methods in cancer research, volume II: The design and analysis of cohort
    studies. Lyon: International Agency for Research on Cancer, World Health Organisation; 1987.
    [2] Armitage P, Berry G. Statistical methods in medical research (4th edn). Oxford: Blackwell; 2002.

    :param observed_deaths: Number observed events within an area
    :param population: Series or array or list of the population within which the events occurred
    :param reference_deaths:
    :param reference_population: Series or array or list of reference populations to standardise to
    :param multiplier: Multiplier to normalise output (default to 100)
    :param metadata: A dictionary of metadata used in this calculation; confidence, statistic & method. Default to True
    :param alpha: Alpha - default 0.05 for 95% confidence intervals
    :return: The indirectly standardised rate, lower, and upper confidence intervals as a tuple
    """
    validate_data(multiplier=multiplier, metadata=metadata, alpha=alpha)
    validate_arrays([observed_deaths, population, reference_deaths, reference_population], obs_array=observed_deaths,
                    pop_array=population)

    frame = pd.DataFrame(np.column_stack([reference_population, reference_deaths, population]),
                         columns=['reference_population', 'reference_deaths', 'population'])

    frame['deaths_per_million'] = (frame['reference_deaths'] / frame['reference_population']) * 1000000
    frame['expected_deaths'] = (frame['population'] * frame['deaths_per_million']) / 1000000
    expected_deaths = frame['expected_deaths'].sum()
    smr = (observed_deaths / expected_deaths) * multiplier
    if observed_deaths < 10:
        cis = exact(smr, alpha=alpha)
        method = 'exact'
    else:
        cis = byars(smr, alpha=alpha)
        method = 'Byars'

    if metadata:
        metadata_to_return = {
            'confidence': str((1 - alpha) * 100) + '%',
            'statistic': 'SMR per ' + str(multiplier),
            'method': method
        }
        return smr, cis[0], cis[1], metadata_to_return

    return smr, cis[0], cis[1]
