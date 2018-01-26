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
from mooquant.barfeed import quandlfeed
from mooquant.utils import csvutils, dt

# http://www.quandl.com/help/api

def download_csv(sourceCode, tableCode, begin, end, frequency, authToken):
    url = "http://www.quandl.com/api/v1/datasets/%s/%s.csv" % (sourceCode, tableCode)
    params = {
        "trim_start": begin.strftime("%Y-%m-%d"),
        "trim_end": end.strftime("%Y-%m-%d"),
        "collapse": frequency
    }

    if authToken is not None:
        params["auth_token"] = authToken

    return csvutils.download_csv(url, params)


def download_daily_bars(sourceCode, tableCode, year, csvFile, authToken=None):
    """Download daily bars from Quandl for a given year.

    :param sourceCode: The dataset's source code.
    :type sourceCode: string.
    :param tableCode: The dataset's table code.
    :type tableCode: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    :param authToken: Optional. An authentication token needed if you're doing more than 50 calls per day.
    :type authToken: string.
    """

    bars = download_csv(sourceCode, tableCode, datetime.date(year, 1, 1), datetime.date(year, 12, 31), "daily",
                        authToken)
    with open(csvFile, "w") as f:
        f.write(bars)


def download_weekly_bars(sourceCode, tableCode, year, csvFile, authToken=None):
    """Download weekly bars from Quandl for a given year.

    :param sourceCode: The dataset's source code.
    :type sourceCode: string.
    :param tableCode: The dataset's table code.
    :type tableCode: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    :param authToken: Optional. An authentication token needed if you're doing more than 50 calls per day.
    :type authToken: string.
    """

    begin = dt.get_first_monday(year) - datetime.timedelta(days=1)  # Start on a sunday
    end = dt.get_last_monday(year) - datetime.timedelta(days=1)  # Start on a sunday
    bars = download_csv(sourceCode, tableCode, begin, end, "weekly", authToken)

    with open(csvFile, "w") as f:
        f.write(bars)


def build_feed(sourceCode, tableCodes, fromYear, toYear, storage, frequency=bar.Frequency.DAY, timezone=None,
               skipErrors=False, noAdjClose=False, authToken=None, columnNames={}, forceDownload=False
               ):
    """Build and load a :class:`mooquant.barfeed.quandlfeed.Feed` using CSV files downloaded from Quandl.
    CSV files are downloaded if they haven't been downloaded before.

    :param sourceCode: The dataset source code.
    :type sourceCode: string.
    :param tableCodes: The dataset table codes.
    :type tableCodes: list.
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
    :param noAdjClose: True if the instruments don't have adjusted close values.
    :type noAdjClose: boolean.
    :param authToken: Optional. An authentication token needed if you're doing more than 50 calls per day.
    :type authToken: string.
    :param columnNames: Optional. A dictionary to map column names. Valid key values are:

        * datetime
        * open
        * high
        * low
        * close
        * volume
        * adj_close

    :type columnNames: dict.

    :rtype: :class:`mooquant.barfeed.quandlfeed.Feed`.
    """

    logger = mooquant.logger.getLogger("quandl")
    ret = quandlfeed.Feed(frequency, timezone)

    if noAdjClose:
        ret.setNoAdjClose()

    # Additional column names.
    for col, name in columnNames.items():
        ret.setColumnName(col, name)

    if not os.path.exists(storage):
        logger.info("Creating %s directory" % (storage))
        os.mkdir(storage)

    for year in range(fromYear, toYear + 1):
        for tableCode in tableCodes:
            fileName = os.path.join(storage, "%s-%s-%d-quandl.csv" % (sourceCode, tableCode, year))

            if not os.path.exists(fileName) or forceDownload:
                logger.info("Downloading %s %d to %s" % (tableCode, year, fileName))
                try:
                    if frequency == bar.Frequency.DAY:
                        download_daily_bars(sourceCode, tableCode, year, fileName, authToken)
                    elif frequency == bar.Frequency.WEEK:
                        download_weekly_bars(sourceCode, tableCode, year, fileName, authToken)
                    else:
                        raise Exception("Invalid frequency")
                except Exception as e:
                    if skipErrors:
                        logger.error(str(e))
                        continue
                    else:
                        raise e

            ret.addBarsFromCSV(tableCode, fileName)

    return ret
