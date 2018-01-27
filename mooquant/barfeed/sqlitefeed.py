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

import os
import sqlite3

from mooquant import bar
from mooquant.barfeed import dbfeed, membf
from mooquant.utils import dt


def normalize_instrument(instrument):
    return instrument.upper()


# SQLite DB.
# Timestamps are stored in UTC.
class Database(dbfeed.Database):
    def __init__(self, dbFilePath):
        self.__instrumentIds = {}

        # If the file doesn't exist, we'll create it and initialize it.
        initialize = False

        if not os.path.exists(dbFilePath):
            initialize = True

        self.__connection = sqlite3.connect(dbFilePath)
        self.__connection.isolation_level = None  # To do auto-commit

        if initialize:
            self.createSchema()

    def __findInstrumentId(self, instrument):
        cursor = self.__connection.cursor()
        sql = "SELECT [instrument_id] FROM [instrument] WHERE [name] = ?"
        cursor.execute(sql, [instrument])
        ret = cursor.fetchone()

        if ret is not None:
            ret = ret[0]

        cursor.close()

        return ret

    def __addInstrument(self, instrument):
        ret = self.__connection.execute("INSERT INTO [instrument] ([name]) VALUES (?)", [instrument])
        return ret.lastrowid

    def __getOrCreateInstrument(self, instrument):
        # Try to get the instrument id from the cache.
        ret = self.__instrumentIds.get(instrument, None)

        if ret is not None:
            return ret

        # If its not cached, get it from the db.
        ret = self.__findInstrumentId(instrument)

        # If its not in the db, add it.
        if ret is None:
            ret = self.__addInstrument(instrument)

        # Cache the id.
        self.__instrumentIds[instrument] = ret
        return ret

    def createSchema(self):
        self.__connection.execute(
            "CREATE TABLE instrument ("
            "instrument_id INTEGER PRIMARY KEY AUTOINCREMENT"
            ", name TEXT UNIQUE NOT NULL)")

        self.__connection.execute(
            "CREATE TABLE bar ("
            "instrument_id INTEGER REFERENCES instrument (instrument_id)"
            ", frequency INTEGER NOT NULL"
            ", timestamp INTEGER NOT NULL"
            ", open REAL NOT NULL"
            ", high REAL NOT NULL"
            ", low REAL NOT NULL"
            ", close REAL NOT NULL"
            ", volume REAL NOT NULL"
            ", adj_close REAL"
            ", PRIMARY KEY (instrument_id, frequency, timestamp))")

    def addBar(self, instrument, bar, frequency):
        instrument = normalize_instrument(instrument)
        instrumentId = self.__getOrCreateInstrument(instrument)
        timeStamp = dt.datetime_to_timestamp(bar.getDateTime())

        try:
            sql = "INSERT INTO bar (instrument_id, frequency, timestamp, open, high, low, close, volume, adj_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = [instrumentId, frequency, timeStamp, bar.getOpen(), bar.getHigh(), bar.getLow(), bar.getClose(),
                      bar.getVolume(), bar.getAdjClose()]
            self.__connection.execute(sql, params)
        except sqlite3.IntegrityError:
            sql = "UPDATE bar SET open = ?, high = ?, low = ?, close = ?, volume = ?, adj_close = ?" \
                  " WHERE instrument_id = ? AND frequency = ? AND timestamp = ?"
            params = [bar.getOpen(), bar.getHigh(), bar.getLow(), bar.getClose(), bar.getVolume(), bar.getAdjClose(),
                      instrumentId, frequency, timeStamp]
            self.__connection.execute(sql, params)

    def getBars(self, instrument, frequency, timezone=None, fromDateTime=None, toDateTime=None):
        instrument = normalize_instrument(instrument)
        sql = "SELECT bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume, bar.adj_close, bar.frequency" \
              " FROM bar JOIN instrument ON (bar.instrument_id = instrument.instrument_id)" \
              " WHERE instrument.name = ? AND bar.frequency = ?"
        args = [instrument, frequency]

        if fromDateTime is not None:
            sql += " AND bar.timestamp >= ?"
            args.append(dt.datetime_to_timestamp(fromDateTime))

        if toDateTime is not None:
            sql += " AND bar.timestamp <= ?"
            args.append(dt.datetime_to_timestamp(toDateTime))

        ret = []
        sql += " ORDER by bar.timestamp ASC"
        
        cursor = self.__connection.cursor()
        cursor.execute(sql, args)

        for row in cursor:
            dateTime = dt.timestamp_to_datetime(row[0])

            if timezone:
                dateTime = dt.localize(dateTime, timezone)

            ret.append(bar.BasicBar(dateTime, row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

        cursor.close()
        return ret

    def disconnect(self):
        self.__connection.close()
        self.__connection = None


class Feed(membf.BarFeed):
    def __init__(self, dbFilePath, frequency, maxLen=None):
        super(Feed, self).__init__(frequency, maxLen)
        self.__db = Database(dbFilePath)

    def barsHaveAdjClose(self):
        return True

    def getDatabase(self):
        return self.__db

    def loadBars(self, instrument, timezone=None, fromDateTime=None, toDateTime=None):
        bars = self.__db.getBars(instrument, self.getFrequency(), timezone, fromDateTime, toDateTime)
        self.addBarsFromSequence(instrument, bars)
