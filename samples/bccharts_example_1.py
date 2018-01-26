from mooquant.provider.bitcoincharts import barfeed
from mooquant.tools import resample
from mooquant import bar

import datetime


def main():
    barFeed = barfeed.CSVTradeFeed()
    barFeed.addBarsFromCSV("../tests/data/bitstampUSD.csv", fromDateTime=datetime.datetime(2014, 1, 1))
    resample.resample_to_csv(barFeed, bar.Frequency.MINUTE*30, "30min-bitstampUSD.csv")


if __name__ == "__main__":
    main()
