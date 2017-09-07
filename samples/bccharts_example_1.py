# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import datetime

from mooquant import bar
from mooquant.bitcoincharts import barfeed
from mooquant.tools import resample


def main():
    barFeed = barfeed.CSVTradeFeed()
    barFeed.addBarsFromCSV("bitstampUSD.csv", fromDateTime=datetime.datetime(2014, 1, 1))
    resample.resample_to_csv(barFeed, bar.Frequency.MINUTE*30, "30min-bitstampUSD.csv")


if __name__ == "__main__":
    main()
