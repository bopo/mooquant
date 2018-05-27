import itertools

from mooquant.optimizer import local
from mooquant.tools import tushare
from samples import rsi2


def parameters_generator(instrument):
    instrument = [instrument]
    entrySMA = list(range(150, 251))
    exitSMA = list(range(5, 16))
    rsiPeriod = list(range(2, 11))
    overBoughtThreshold = list(range(75, 96))
    overSoldThreshold = list(range(5, 26))
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)


# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    # Load the feed from the CSV files.
    # feed = yahoofeed.Feed()
    # feed.addBarsFromCSV("dia", "./tests/data/DIA-2009-yahoofinance.csv")
    # feed.addBarsFromCSV("dia", "./tests/data/DIA-2010-yahoofinance.csv")
    # feed.addBarsFromCSV("dia", "./tests/data/DIA-2011-yahoofinance.csv")

    instrument = '600016'
    feed = tushare.build_feed([instrument], 2016, 2018, './histdata/tushare')

    local.run(rsi2.RSI2, feed, parameters_generator(instrument))
