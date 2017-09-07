#!/usr/bin/env python

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
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='MooQuant',
    version='0.1.0',
    description='MooQuant',
    long_description='Python library for backtesting stock trading strategies.',
    author='Bopo Wang',
    author_email='ibopo@126.com',
    url='http://www.mooquant.com/',
    download_url='http://www.mooquant.com/0.1.0/MooQuant-0.1.0.tar.gz/download',
    packages=[
        'mooquant',
    ],
    install_requires=[
        "python-dateutil",
        "requests",
        "numpy",
        "pytz",
    ],
    extras_require={
        'Scipy':  ["scipy"],
        'TALib':  ["Cython", "TA-Lib"],
        'Plotting':  ["matplotlib"],
        'Bitstamp':  ["ws4py>=0.3.4", "tornado"],
        # 'Twitter':  ["tweepy"],
    },
)
