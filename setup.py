from setuptools import setup

setup(
    name='PHStatsMethods',
    version='0.1.5',
    packages=['PHStatsMethods'],
    url='https://github.com/DataS-DHSC/PHStatsMethods',
    license='GPL3',
    author='Department of Health and Social Care',
    author_email='annabel.westermann@dhsc.gov.uk, hadley.nanayakkara@dhsc.gov.uk, cameron.stewart@dhsc.gov.uk, jack.burden@dhsc.gov.uk, thilaksan.vikneswaran@dhsc.gov.uk, paul.fryers@dhsc.gov.uk, phds@phe.gov.uk',
    description='This is a python package to calculate statistics in public health, including indicators for Fingertips.',
    long_description='This is a python package to calculate statistics in public health, including indicators for Fingertips.',
    install_requires=['numpy >= 1.24.0',
                      'pandas >= 2.0.0',
                      'pytest >= 8.0.0',
                      'scipy >= 1.8.0',
                      'openpyxl >= 3.1.0'],
)

