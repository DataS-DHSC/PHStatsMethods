

def validate_data(numerator=None, denominator=None, multiplier=None, metadata=None, alpha=None):
    """
    Function to validate the data inputs to the base functions
    :param numerator: Numerator value passed into function
    :param denominator: Denominator value passed into function
    :param multiplier: Multiplier value passed into function
    :param metadata: Metadata value passed into function
    :param alpha: Alpha value passed into function
    :return:
    """
    if numerator and not isinstance(numerator, (int, float, complex)):
        raise TypeError('Numerators need to be numerical')
    if numerator and numerator < 0:
        raise ValueError('Numerator has to be positive or 0')
    if denominator and not isinstance(denominator, (int, float, complex)):
        raise TypeError('Denominators need to be numerical')
    if denominator and numerator > denominator:
        raise ValueError('Denominator cannot be smaller than numerator')
    if denominator and denominator <= 0:
        raise ValueError('Denominator must be a positive number')
    if multiplier and not isinstance(metadata, (int, float, complex)):
        raise TypeError('Multipliers must be numerical')
    if multiplier and multiplier < 0:
        raise ValueError('Multiplier must be positive')
    if metadata and not isinstance(metadata, bool):
        raise TypeError('Metadata must be either True or False')
    if alpha and not isinstance(alpha, float):
        raise TypeError('Alpha should be numerical between 0 and 0.1 to calculate confidence intervals')
    if alpha and alpha < 0 or alpha > 0.1:
        raise ValueError('Confidence intervals can only be counted with an alpha between 0 and 0.1')
    return


def validate_arrays(array_list, obs_array=None, pop_array=None):
    """
    A function to validate the arrays passed into the DSR, ISR, SMR functions
    :param array_list: A list of the arrays that are required to be the same length
    :param obs_array: The observed values array
    :param pop_array: The local population array
    :return:
    """
    for array in array_list:
        if not all(isinstance(item, (int, float, complex)) for item in array):
            raise TypeError('All items in lists and arrays are required to be numerical')
        if not all(item > -1 for item in array):
            raise ValueError('All items in lists and arrays are required to be positive or 0')
    if not all(len(array) == len(array_list[0]) for array in array_list):
        raise AttributeError('Length of arrays must match')
    if obs_array and pop_array:
        for i in range(len(obs_array)):
            if obs_array[i] > pop_array[i]:
                raise ValueError('Observed values must be smaller than the population from which they were drawn')
    return


def check_dataframe_for_errors(df):
    """
    Tests data frame for errors and stops the process if any of the calculation rules are violated

    :param df: Data frame object from another function
    :return:
    """
    # check for numbers below 0
    negative_numbers = (df < 0).any()
    if (negative_numbers == True).any():
        raise ValueError('No Negative numbers can be used to calculate these statistics')

    # check to see if count is greater than local population
    count_greater_than_local_pop = df[df.iloc[:, 0] > df.iloc[:, 1]].any()
    if (count_greater_than_local_pop == True).any():
        raise ValueError('One or more records have counts greater than the local population')

    # check for 0s in standard population
    if 'stdpop' in df.columns:
        if (df['stdpop'] == 0).any():
            raise ValueError('The standard population cannot have values of 0')
    return
