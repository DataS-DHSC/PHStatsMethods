from setuptools import setup


setup(
    name='ph_statistical_methods',
    version='0.1.2',
    packages=['ph_statistical_methods'],
    url='https://gitlab.phe.gov.uk/Russell.Plunkett/phe-indicator-methods.git',
    license='',
    author='Department of health and Social Care',
    author_email='russell.plunkett@phe.gov.uk, phds@phe.gov.uk',
    description='This is a python package to calculate outputs used in the production of indicators within PHE.',
    install_requires=['pandas>=1.5', 'scipy', 'numpy', 'pytest']
)
