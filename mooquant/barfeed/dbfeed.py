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


# 数据库数据操作 增删改查
class Database(object):
    """ 数据库数据操作 增删改查 """

    def addBars(self, bars, frequency):
        for instrument in bars.getInstruments():
            bar = bars.getBar(instrument)
            self.addBar(instrument, bar, frequency)

    def addBarsFromFeed(self, feed):
        for dateTime, bars in feed:
            if bars:
                self.addBars(bars, feed.getFrequency())

    def addBar(self, instrument, bar, frequency):
        raise NotImplementedError()

    def getBars(self, instrument, frequency, timezone=None, fromDateTime=None, toDateTime=None):
        raise NotImplementedError()
