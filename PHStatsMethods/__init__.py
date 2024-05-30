"""
PHStatsMethods
==============

Introduction
------------
This is a Python package to support analysts in the execution of statistical
methods approved for use in the production of Public Health indicators such as
those presented via `Fingertips <https://fingertips.phe.org.uk/>`__. It
provides functions for the generation of Proportions, Rates, DSRs, ISRs,
Funnel plots and Means including confidence intervals for these statistics,
and a function for assigning data to quantiles.

Any feedback would be appreciated and can be provided using the Issues
section of the `PHStatsMethods GitHub
repository <https://github.com/DataS-DHSC/PHStatsMethods/issue>`__.

Licence
-------
This project is released under the `GPL-3 <https://opensource.org/licenses/GPL-3.0>`__
licence.

Examples
--------
Below is a example using the ph_proportion() function to demonstrate the purpose of
package. 

>>> df = pd.DataFrame({'area': ["Area1", "Area2", "Area3", "Area4"] * 3,
                       'numerator': [None, 48, 10000, 7, 82, 6500, 10000, 750, 9, 8200, 8, 900],
                       'denominator': [100, 10000, 10000, 10000] * 3})

Ungrouped 

  >>> PHStatsMethods.ph_proportion(df, 'numerator', 'denominator')

Grouped

  >>> PHStatsMethods.ph_proportion(df, 'numerator', 'denominator', 'area', multiplier = 100)

For more information on any function, you can use:

  >>> help(PHStatsMethods.function)

"""

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

__all__ = ["wilson_lower", "wilson_upper", "wilson",
           "exact_upper", "exact_lower", "exact",
           "byars_lower", "byars_upper", "byars", 
           "dobson_lower", "dobson_upper", "student_t_dist", 
           "calculate_funnel_limits", "assign_funnel_significance", "calculate_funnel_points",
           "ph_dsr", "ph_ISRate", "ph_ISRatio", "ph_mean", "ph_proportion",
           "ph_quantile", "ph_rate", "euro_standard_pop"]