#!/usr/bin/env python
from setuptools import setup, find_packages
from os.path import abspath, dirname, join

setup_dir = dirname(abspath(__file__))
README = open(join(setup_dir, 'README.md')).read()

CLASSIFIERS = [
    'Development Status :: 1 - Beta',
    'Intended Audience :: Developers',
    'License :: MIT',
    'Operating System :: Unix',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Utilities',
]

setup(
    name='faker_pandas',
    version='0.1.0',
    license='MIT',
    description='Adds Provider for Faker library to Generate randomized Pandas DataFrames',
    long_description=README,
    author='Sani',
    author_email='sani@sani.love',
    url='https://github.com/nitori/faker_pandas',
    packages=find_packages('faker_pandas'),
    package_dir={'': 'faker_pandas'},
    include_package_data=True,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    project_urls={
        'Issue Tracker': 'https://github.com/nitori/faker_pandas/issues',
    },
    python_requires='>=3.9',
    install_requires=['Faker>=13.6.0', 'pandas>=1.4.2'],
    test_requires=['pytest>=7.1.2'],
)
