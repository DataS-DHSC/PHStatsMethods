# PH_statistical_methods
This is a Python package to support analysts in the execution of statistical
methods approved for use in the production of Public Health indicators such as
those presented via [Fingertips](https://fingertips.phe.org.uk/). It
provides functions for the generation of Proportions, Rates, DSRs, ISRs,
Means and Life Expectancy including confidence intervals for these statistics,
and a function for assigning data to quantiles.

Any feedback would be appreciated and can be provided using the Issues
section of the [PH_statistical_methods GitHub
repository](https://github.com/DataS-DHSC/PH_statistical_methods/issues).


## Installation
This packaged should be installed using pip:

    pip install PH_statistical_methods

Or it can be compiled from source (still requires pip):

    pip install git+https://github.com/DataS-DHSC/PH_statistical_methods.git

## Usage
PH_statistical_methods should be imported and used in line with standard python
conventions. It is suggested that if the whole package is to be imported 
then the following convention is used:
 
    import PH_statistical_methods as phm

For more information on any function, you can use:

    help(*PH_statistical_methods function name*)

## Licence
This project is released under the [GPL-3](https://opensource.org/licenses/GPL-3.0)
licence.
