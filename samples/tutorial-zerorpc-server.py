import itertools

from mooquant.optimizer import server
from mooquant.tools import mootdx


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
    # feeds = yahoofeed.Feed()
    # feeds.addBarsFromCSV("dia", "./tests/data/DIA-2009-yahoofinance.csv")
    # feeds.addBarsFromCSV("dia", "./tests/data/DIA-2010-yahoofinance.csv")
    # feeds.addBarsFromCSV("dia", "./tests/data/DIA-2011-yahoofinance.csv")

    instrument = '600036'
    feeds = mootdx.build_feed([instrument], 2003, 2018, './histdata/mootdx')

    # Run the server.
    server.serve(
        strategyParameters=parameters_generator(instrument),
        address="0.0.0.0",
        barFeed=feeds,
        drivce='zmq',
        port=5000
    )
