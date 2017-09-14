# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import itertools

import rsi2
from mooquant.barfeed import yahoofeed
from mooquant.optimizer import local


def parameters_generator():
    instrument = ["dia"]
    entrySMA = range(150, 251)
    exitSMA = range(5, 16)
    rsiPeriod = range(2, 11)
    overBoughtThreshold = range(75, 96)
    overSoldThreshold = range(5, 26)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)


# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    # Load the feed from the CSV files.
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("dia", "data/dia-2009.csv")
    feed.addBarsFromCSV("dia", "data/dia-2010.csv")
    feed.addBarsFromCSV("dia", "data/dia-2011.csv")

    local.run(rsi2.RSI2, feed, parameters_generator())
