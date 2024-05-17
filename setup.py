from setuptools import setup


setup(
    name='PHStatsMethods',
    version='0.1.3',
    packages=['ph_statistical_methods'],
    url='https://github.com/DataS-DHSC/PH_statistical_methods',
    license='',
    author='Department of Health and Social Care',
    author_email='annabel.westermann@dhsc.gov.uk, phds@phe.gov.uk',
    description='This is a python package to calculate statistics in public health, including indicators for Fingertips.',
    install_requires=['numpy >= 1.25.0',
                      'pandas >= 2.0.0',
                      'pytest >= 8.0.0',
                      'scipy >= 1.8.0',
                      'openpyxl >= 3.1.0']
)

