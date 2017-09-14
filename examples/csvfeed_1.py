# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

from mooquant.feed import csvfeed

feed = csvfeed.Feed("Date", "%Y-%m-%d")
feed.addValuesFromCSV("data/quandl_gold_2.csv")

for dateTime, value in feed:
    print(dateTime, value)
