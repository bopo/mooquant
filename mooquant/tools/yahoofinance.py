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
from mooquant.barfeed import yahoofeed
from mooquant.utils import csvutils, dt


def __adjust_month(month):
    if month > 12 or month < 1:
        raise Exception("Invalid month")

    month -= 1  # Months for yahoo are 0 based
    return month


def download_csv(instrument, begin, end, frequency):
    url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=%s&ignore=.csv" % (
        instrument, __adjust_month(begin.month), begin.day, begin.year, __adjust_month(end.month), end.day, end.year,
        frequency)

    return csvutils.download_csv(url)


def download_daily_bars(instrument, year, csvFile):
    """Download daily bars from Yahoo! Finance for a given year.

    :param instrument: Instrument identifier.
    :type instrument: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    """

    bars = download_csv(instrument, datetime.date(year, 1, 1), datetime.date(year, 12, 31), "d")

    with open(csvFile, "w") as f:
        f.write(bars)


def download_weekly_bars(instrument, year, csvFile):
    """Download weekly bars from Yahoo! Finance for a given year.

    :param instrument: Instrument identifier.
    :type instrument: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    """

    begin = dt.get_first_monday(year)
    end = dt.get_last_monday(year) + datetime.timedelta(days=6)
    bars = download_csv(instrument, begin, end, "w")

    with open(csvFile, "w") as f:
        f.write(bars)


def build_feed(instruments, fromYear, toYear, storage, frequency=bar.Frequency.DAY, timezone=None, skipErrors=False):
    """Build and load a :class:`mooquant.barfeed.yahoofeed.Feed` using CSV files downloaded from Yahoo! Finance.
    CSV files are downloaded if they haven't been downloaded before.

    :param instruments: Instrument identifiers.
    :type instruments: list.
    :param fromYear: The first year.
    :type fromYear: int.
    :param toYear: The last year.
    :type toYear: int.
    :param storage: The path were the files will be loaded from, or downloaded to.
    :type storage: string.
    :param frequency: The frequency of the bars. Only **mooquant.bar.Frequency.DAY** or **mooquant.bar.Frequency.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`mooquant.marketsession`.
    :type timezone: A pytz timezone.
    :param skipErrors: True to keep on loading/downloading files in case of errors.
    :type skipErrors: boolean.
    :rtype: :class:`mooquant.barfeed.yahoofeed.Feed`.
    """

    logger = mooquant.logger.getLogger("yahoofinance")
    ret = yahoofeed.Feed(frequency, timezone)

    if not os.path.exists(storage):
        logger.info("Creating %s directory" % (storage))
        os.mkdir(storage)

    for year in range(fromYear, toYear + 1):
        for instrument in instruments:
            fileName = os.path.join(storage, "%s-%d-yahoofinance.csv" % (instrument, year))
            if not os.path.exists(fileName):
                logger.info("Downloading %s %d to %s" % (instrument, year, fileName))
                try:
                    if frequency == bar.Frequency.DAY:
                        download_daily_bars(instrument, year, fileName)
                    elif frequency == bar.Frequency.WEEK:
                        download_weekly_bars(instrument, year, fileName)
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
