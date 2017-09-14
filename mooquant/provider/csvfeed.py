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
from datetime import datetime

import pandas as pd

from mooquant import dataseries
from mooquant.barfeed import membf
from mooquant.barfeed.pandasfeed import dataframeToBar, dataframeToTick


class Feed(membf.BarFeed):
    def __init__(self, frequency, maxLen=dataseries.DEFAULT_MAX_LEN):
        membf.BarFeed.__init__(self, frequency, maxLen)
        self.__frequency = frequency

    def barsHaveAdjClose(self):
        return False

    def setDateTimeFormat(self, iformat):
        self._datetime_format = iformat

    def loadBars(self, instrument, exchange_id, fromdate, todate, path):
        try:
            fromdate = datetime.strptime(fromdate, '%Y%m%d')
            todate = datetime.strptime(todate, '%Y%m%d')
        except Exception:
            raise Exception('invalid date format, e.g. 20160206')

        idataframe = pd.read_csv(path)
        idataframe.ix[:, 'datetime'] = idataframe.ix[:, 'datetime'].apply(
            lambda x: datetime.strptime(x, self._datetime_format))
        idataframe = idataframe[(idataframe.datetime >= fromdate) & (idataframe.datetime <= todate)]
        bars = dataframeToBar(idataframe, self.__frequency)
        mooquant_id = instrument + '.' + exchange_id

        self.addBarsFromSequence(mooquant_id, bars)

    def loadTicks(self, instrument, exchange_id, fromdate, todate, path):
        try:
            fromdate = datetime.strptime(fromdate, '%Y%m%d')
            todate = datetime.strptime(todate, '%Y%m%d')
        except Exception:
            raise Exception('invalid date format, e.g. 20160206')

        idataframe = pd.read_csv(path)
        idataframe = idataframe.sort_values(by='datetime')
        idataframe.ix[:, 'datetime'] = idataframe.ix[:, 'datetime'].apply(
            lambda x: datetime.strptime(x, self._datetime_format))
        idataframe = idataframe[(idataframe.datetime >= fromdate) & (idataframe.datetime <= todate)]
        bars = dataframeToTick(idataframe, self.__frequency)
        mooquant_id = instrument + '.' + exchange_id

        self.addBarsFromSequence(mooquant_id, bars)

    def closeDB(self):
        self.__db.closeDB()
