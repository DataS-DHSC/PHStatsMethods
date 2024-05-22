__all__ = ["wilson_lower", "wilson_upper", "wilson",
           "exact_upper", "exact_lower", "exact",
           "byars_lower", "byars_upper", "byars", 
           "dobson_lower", "dobson_upper", "student_t_dist", 
           "calculate_funnel_limits", "assign_funnel_significance", "calculate_funnel_points"
           "ph_dsr", "ph_ISRate", "ph_ISRatio", "ph_mean", "ph_proportion",
           "ph_quantile", "ph_rate", "euro_standard_pop"]

from .confidence_intervals import *
from .DSR import ph_dsr
from .funnels import calculate_funnel_limits, assign_funnel_significance, calculate_funnel_points
from .ISRate import ph_ISRate
from .ISRatio import ph_ISRatio
from .means import ph_mean
from .proportions import ph_proportion
from .quantiles import ph_quantile
from .rates import ph_rate
from .utils import euro_standard_pop

"""
This is a Python package to support analysts in the execution of statistical
methods approved for use in the production of Public Health indicators such as
those presented via `Fingertips <https://fingertips.phe.org.uk/>`__. It
provides functions for the generation of Proportions, Rates, DSRs, ISRs,
Funnel plots and Means including confidence intervals for these statistics,
and a function for assigning data to quantiles.

Any feedback would be appreciated and can be provided using the Issues
section of the `PHStatsMethods GitHub
repository <https://github.com/DataS-DHSC/PHStatsMethods/issue>`__.

For more information on any function, you can use:

    help(*phm.function*)

Licence:
    This project is released under the `GPL-3 <https://opensource.org/licenses/GPL-3.0>`__
    licence.

"""