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
import pandas as pd

from mooquant import dataseries
from mooquant.barfeed import membf
from mooquant.providers import bar


def dataframeToBar(bar_dataframe, frequency):
    bars = []

    for _, row in bar_dataframe.iterrows():
        tmp_extra = {}

        for key in row.keys():
            if key not in ['datetime', 'open', 'high', 'low', 'close', 'volume', 'amount']:
                tmp_extra[key] = row[key]
        
        bars.append(bar.BasicBar(row['datetime'], row['open'], row['high'], row['low'], row['close'], row['volume']\
                 , row['amount'], frequency, False, tmp_extra))
    
    return bars
    
    
def dataframeToTick(tick_dataframe, frequency):
    ticks = []

    for _, row in tick_dataframe.iterrows():
        tmp_extra = {}
        tmp_ap = {}
        tmp_bp = {}
        tmp_av = {}
        tmp_bv = {}

        for key in row.keys():
            #extract order book component 
            if key[:2] == 'ap':
                tmp_ap[int(key[2:])] = row[key]
                continue
                
            elif key[:2] == 'bp':
                tmp_bp[int(key[2:])] = row[key]
                continue

            elif key[:2] == 'av':
                tmp_av[int(key[2:])] = row[key]
                continue
                
            elif key[:2] == 'bv':
                tmp_bv[int(key[2:])] = row[key]
                continue                
                
            #extract extra component
            if key not in ['datetime', 'open', 'high', 'low', 'close', 'volume', 'amount', 'preclose'\
                         , 'new_price', 'bought_amount', 'sold_amount', 'bought_volume', 'sold_volume'\
                         , 'frequency']:
                tmp_extra[key] = row[key]

                
        ticks.append(bar.BasicTick(row['datetime'], row['open'], row['high'], row['low'], row['close'], row['volume']\
                 , row['amount'], tmp_bp, tmp_bv, tmp_ap, tmp_av, row['preclose'], row['bought_volume']\
                 , row['sold_volume'], row['bought_amount'], row['sold_amount'], frequency, False, tmp_extra))
    
    return ticks

    
class Feed(membf.BarFeed):
    def __init__(self, frequency, maxLen=dataseries.DEFAULT_MAX_LEN):
        membf.BarFeed.__init__(self, frequency, maxLen)
        self.__frequency = frequency
        
    def barsHaveAdjClose(self):
        return False

    def loadBars(self, instrument_id, exchange_id, idataframe):         
        bars = dataframeToBar(idataframe, self.__frequency)
        mooquant_id = instrument_id + '.' + exchange_id
        self.addBarsFromSequence(mooquant_id, bars)
            
    def closeDB(self):
        self.__db.closeDB()
