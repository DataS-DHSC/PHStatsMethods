.. PHStatsMethods documentation master file, created by
   sphinx-quickstart on Wed May 29 10:29:43 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PHStatsMethods's documentation!
==========================================

Introduction
============


This is a Python package to support analysts in the execution of statistical
methods approved for use in the production of Public Health indicators such as
those presented via [Fingertips](https://fingertips.phe.org.uk/). It
provides functions for the generation of Proportions, Rates, DSRs, ISRs,
Funnel plots and Means including confidence intervals for these statistics,
and a function for assigning data to quantiles.

Any feedback would be appreciated and can be provided using the Issues
section of the [PHStatsMethods GitHub
repository](https://github.com/DataS-DHSC/PHStatsMethods/issues).


Installation
************

This packaged should be installed using pip:

```
pip install PHStatsMethods
```

Or it can be compiled from source (still requires pip):

```
pip install git+https://github.com/DataS-DHSC/PHStatsMethods.git
```

Usage
*****
PH_statistical_methods should be imported and used in line with standard python
conventions. It is suggested that if the whole package is to be imported 
then one of the two the following conventions are used:

  >>> import PHStatsMethods

  >>> from PHStatsMethods import *

For more information on any function, you can use:

  >>> help(PHStatsMethods.function)

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


Licence
*******
This project is released under the [GPL-3](https://opensource.org/licenses/GPL-3.0)
licence.

Functions
*********

.. automodule:: PHStatsMethods.proportions
   :members:
.. automodule:: PHStatsMethods.rates
   :members:
.. automodule:: PHStatsMethods.means
   :members:
.. automodule:: PHStatsMethods.DSR
   :members:
.. automodule:: PHStatsMethods.ISRate
   :members:
.. automodule:: PHStatsMethods.ISRatio
   :members:
.. automodule:: PHStatsMethods.quantiles
   :members:
.. automodule:: PHStatsMethods.funnels
   :members:
.. automodule:: PHStatsMethods.confidence_intervals
   :members:
.. automodule:: PHStatsMethods.utils
   :members:

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   PHStatsMethods/README.md



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`