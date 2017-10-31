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

from mooquant import analyzer


# 最大回撤率辅助类
# https://baike.baidu.com/item/%E6%9C%80%E5%A4%A7%E5%9B%9E%E6%92%A4%E7%8E%87/3645063?fr=aladdin
class DrawDownHelper(object):
    """A :class: `mooquant.analyzer.DrawDownHelper`
    最大回撤率"""

    def __init__(self):
        self.__highWatermark = None
        self.__lowWatermark = None
        self.__lastLow = None
        self.__highDateTime = None
        self.__lastDateTime = None

    # 持续时间
    # The drawdown duration, not necessarily the max drawdown duration.
    def getDuration(self):
        return self.__lastDateTime - self.__highDateTime

    # 获取最大回撤率
    def getMaxDrawDown(self):
        """获取最大回撤率"""
        return (self.__lowWatermark - self.__highWatermark) / float(self.__highWatermark)

    # 获取当前回撤率
    def getCurrentDrawDown(self):
        """获取当前回撤率"""
        return (self.__lastLow - self.__highWatermark) / float(self.__highWatermark)

    # 更新操作
    def update(self, dateTime, low, high):
        assert (low <= high)

        self.__lastLow = low
        self.__lastDateTime = dateTime

        if self.__highWatermark is None or high >= self.__highWatermark:
            self.__highWatermark = high
            self.__lowWatermark = low
            self.__highDateTime = dateTime
        else:
            self.__lowWatermark = min(self.__lowWatermark, low)


# 回撤
class DrawDown(analyzer.StrategyAnalyzer):
    """A :class:`mooquant.analyzer.StrategyAnalyzer` that calculates
    max. drawdown and longest drawdown duration for the portfolio."""

    def __init__(self):
        super(DrawDown, self).__init__()
        self.__maxDD = 0
        self.__longestDDDuration = datetime.timedelta()
        self.__currDrawDown = DrawDownHelper()

    # 计算(calculate)股权(Equity)
    def calculateEquity(self, strat):
        return strat.getBroker().getEquity()

    # bars 之前操作
    def beforeOnBars(self, strat, bars):
        equity = self.calculateEquity(strat)
        self.__currDrawDown.update(bars.getDateTime(), equity, equity)
        self.__longestDDDuration = max(self.__longestDDDuration, self.__currDrawDown.getDuration())
        self.__maxDD = min(self.__maxDD, self.__currDrawDown.getMaxDrawDown())

    # 获取最大回撤
    def getMaxDrawDown(self):
        """Returns the max. (deepest) drawdown."""
        return abs(self.__maxDD)

    # 获得最长的回撤持续时间
    def getLongestDrawDownDuration(self):
        """Returns the duration of the longest drawdown.

        :rtype: :class:`datetime.timedelta`.

        .. note::
            Note that this is the duration of the longest drawdown, not necessarily the deepest one.
        """
        return self.__longestDDDuration
