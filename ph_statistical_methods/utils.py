# -*- coding: utf-8 -*-

from scipy.special import ndtri


def get_calc_variables(a):
    """
    Creates the cumulative normal distribution and z score for a given alpha

    :param a: alpha
    :return: cumulative normal distribution, z score
    """
    norm_cum_dist = ndtri((100 + (100 - (100 * a))) / 200)
    z = ndtri(1 - a / 2)
    return norm_cum_dist, z