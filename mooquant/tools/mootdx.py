# -*- coding: utf-8 -*-
# MooQuant
#
# Copyright 2017 bopo.wang<ibopo@126.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: bopo.wang <ibopo@126.com>
"""

import datetime
import os

import mooquant.logger
from mooquant import bar
from mooquant.barfeed import mootdxfeed
from mooquant.utils import csvutils
from mootdx import quotes

def download_csv(instrument, begin, end):
    quote = quotes.Quotes()
    return quote.k(instrument, begin, end)

def download_daily_bars(instrument, year, csvFile):
    """Download daily bars from Google Finance for a given year.

    :param instrument: Instrument identifier.
    :type instrument: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    """

    begin = datetime.date(year, 1, 1).strftime('%Y-%m-%d')
    end = datetime.date(year, 12, 31).strftime('%Y-%m-%d')
    bars = download_csv(instrument, begin, end)

    if len(bars) > 0:
        bars = bars.drop(['code'], axis=1)
        bars.columns = ['Open', 'Close', 'High', 'Low', 'Volume', 'Amount', 'Date']
        bars.to_csv(csvFile, encoding='utf-8', index=False)


def build_feed(instruments, fromYear, toYear, storage, frequency=bar.Frequency.DAY, timezone=None, skipErrors=False):
    """Build and load a :class:`mooquant.barfeed.mootdxfeed.Feed` using CSV files downloaded from Google Finance.
    CSV files are downloaded if they haven't been downloaded before.

    :param instruments: Instrument identifiers.
    :type instruments: list.
    :param fromYear: The first year.
    :type fromYear: int.
    :param toYear: The last year.
    :type toYear: int.
    :param storage: The path were the files will be loaded from, or downloaded to.
    :type storage: string.
    :param frequency: The frequency of the bars. Only **mooquant.bar.Frequency.DAY** is currently supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`mooquant.marketsession`.
    :type timezone: A pytz timezone.
    :param skipErrors: True to keep on loading/downloading files in case of errors.
    :type skipErrors: boolean.
    :rtype: :class:`mooquant.barfeed.mootdxfeed.Feed`.
    """

    logger = mooquant.logger.getLogger("mootdx")
    ret = mootdxfeed.Feed(frequency, timezone)

    if not os.path.exists(storage):
        logger.info("Creating {dirname} directory".format(dirname=storage))
        os.mkdir(storage)

    for year in range(fromYear, toYear + 1):
        for instrument in instruments:
            fileName = os.path.join(
                storage,
                "{instrument}-{year}-mootdx.csv".format(
                    instrument=instrument, year=year))
            if not os.path.exists(fileName):
                logger.info(
                    "Downloading {instrument} {year} to {filename}".format(
                        instrument=instrument, year=year, filename=fileName))
                try:
                    if frequency == bar.Frequency.DAY:
                        download_daily_bars(instrument, year, fileName)
                    else:
                        raise Exception("Invalid frequency")
                except Exception as e:
                    if skipErrors:
                        logger.error(str(e))
                        continue
                    else:
                        raise e

            ret.addBarsFromCSV(instrument, fileName)

    return ret
