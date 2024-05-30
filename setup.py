from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='PHStatsMethods',
    version='0.1.11',
    packages=['PHStatsMethods'],
    url='https://github.com/DataS-DHSC/PHStatsMethods',
    license='GPL-3.0',
    author='Department of Health and Social Care',
    author_email='annabel.westermann@dhsc.gov.uk, hadley.nanayakkara@dhsc.gov.uk, cameron.stewart@dhsc.gov.uk, jack.burden@dhsc.gov.uk, thilaksan.vikneswaran@dhsc.gov.uk, paul.fryers@dhsc.gov.uk, karandeep.kaur@dhsc.gov.uk, phds@phe.gov.uk',
    description='This is a python package to calculate statistics in public health, including indicators for Fingertips.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy >= 1.24.0',
                      'pandas >= 2.0.0',
                      'pytest >= 8.0.0',
                      'scipy >= 1.8.0',
                      'openpyxl >= 3.1.0'],
)

