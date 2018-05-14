#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MooQuant
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'click>=6.0',
    "python-dateutil",
    "requests",
    "numpy",
    "pytz",
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

from mooquant import __version__

setup(
    name='MooQuant',
    version=__version__,
    description='MooQuant',
    long_description='',
    author='bopowang',
    author_email='ibopo@126.com',
    url='http://www.mooquant.com/',
    download_url='https://github.com/bopo/mooquant/archive/master.zip',
    packages=find_packages(include=['mooquant', 'mooquant.*']),
    extras_require={
        'Scipy': ["scipy"],
        'TALib': ["Cython", "TA-Lib"],
        'Plotting': ["matplotlib"],
        'Bitstamp': ["ws4py>=0.3.4", "tornado==4.5.3"],
    },
    entry_points={
        'console_scripts': [
            'moo = mooquant.cli:main',
            'mooquant = mooquant.cli:main',
        ]
    },
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mooquant',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
