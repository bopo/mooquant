import itertools
from mooquant.barfeed import yahoofeed
from mooquant.optimizer import server


def parameters_generator():
    instrument = ["dia"]
    entrySMA = list(range(150, 251))
    exitSMA = list(range(5, 16))
    rsiPeriod = list(range(2, 11))
    overBoughtThreshold = list(range(75, 96))
    overSoldThreshold = list(range(5, 26))
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    # Load the feed from the CSV files.
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("dia", "../tests/data/DIA-2009-yahoofinance.csv")
    feed.addBarsFromCSV("dia", "../tests/data/DIA-2010-yahoofinance.csv")
    feed.addBarsFromCSV("dia", "../tests/data/DIA-2011-yahoofinance.csv")

    # Run the server.
    server.serve(feed, parameters_generator(), "localhost", 5000)
