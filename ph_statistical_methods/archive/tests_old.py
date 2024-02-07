import pytest
import numpy as np
from ..methods import wilson, wilson_lower, wilson_upper, byars, byars_lower, byars_upper, phe_dsr, \
    european_standard_pop, phe_smr
from ..functions import phe_rate, phe_proportion, phe_mean


def test_byars():
    assert byars(100) == (81.36210549052788, 121.62458755509265)


def test_byars_lower():
    assert byars_lower(100) == 81.36210549052788


def test_byars_upper():
    assert byars_upper(100) == 121.62458755509265


def test_wilson():
    assert wilson(100, 10000) == (0.8229336148148417, 1.2146982255114647)


def test_wilson_lower():
    assert wilson_lower(100, 10000) == 0.8229336148148417


def test_wilson_upper():
    assert wilson_upper(100, 10000) == 1.2146982255114647


obs_array = [50, 55, 55, 55, 60, 60, 65, 70, 70, 70, 70, 65, 60, 55, 50, 40, 25, 15, 10]
pop_array = [509, 559, 559, 559, 609, 609, 659, 709, 709, 709, 709, 659, 609, 559, 509, 409, 259, 159, 109]
reference_events = [60, 65, 65, 65, 70, 70, 75, 80, 80, 80, 80, 75, 70, 65, 60, 50, 35, 25, 20]
smr_test_population = [55, 208, 298, 250, 213, 249, 409, 388, 356, 276, 231, 239, 191, 165, 144, 138, 126, 79]


def test_phe_dsr():
    assert phe_dsr(obs_array, pop_array) == (9832.763039564017, 9232.668299548477, 10461.61759955204)


def test_phe_smr_standard_pops():
    assert phe_smr(30, smr_test_population) == (148.77677430354055, 125.82957137628551, 174.6949196241883)


def test_phe_rate():
    assert phe_rate(100, 10000, 100000) == (1000.0, 813.6210549052789, 1216.2458755509265)


def test_euro_stand_pop():
    np.testing.assert_array_equal(european_standard_pop, [5000, 5500, 5500, 5500, 6000, 6000, 6500, 7000, 7000, 7000,
                                                          7000, 6500, 6000, 5500, 5000, 4000, 2500, 1500, 1000])


wrong_len_obs_array = [50, 55, 55, 55, 70, 70, 70, 65, 60, 55, 50, 40, 25, 15, 10]
wrong_len_pop_array = [509, 559, 559, 659, 709, 709, 709, 709, 659, 609, 559, 509, 409, 259, 159, 109]
wrong_len_reference_events = [65, 65, 70, 70, 75, 80, 80, 80, 80, 75, 70, 65, 60, 50, 35, 25, 20]


def test_list_size_error():
    with pytest.raises(ValueError):
        phe_smr(30, wrong_len_pop_array, wrong_len_reference_events, european_standard_pop)


def test_phe_proportion():
    assert phe_proportion(100, 1000) == (10.0, 8.29094435930957, 12.01519631953484)


def test_phe_mean():
    assert phe_mean(reference_events) == (62.63157894736842, 62.36817934580385, 62.89497854852184)
