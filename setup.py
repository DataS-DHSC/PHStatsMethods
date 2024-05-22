from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name='PHStatsMethods',
    version='0.1.5',
    packages=['PHStatsMethods'],
    url='https://github.com/DataS-DHSC/PHStatsMethods',
    license='GPLv3',
    author='Department of Health and Social Care',
    author_email='annabel.westermann@dhsc.gov.uk, phds@phe.gov.uk',
    description=long_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy >= 1.24.0',
                      'pandas >= 2.0.0',
                      'pytest >= 8.0.0',
                      'scipy >= 1.8.0',
                      'openpyxl >= 3.1.0'],
)

