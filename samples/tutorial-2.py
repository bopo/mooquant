from mooquant import strategy
from mooquant.barfeed import yahoofeed
from mooquant.technical import ma


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        # We want a 15 period SMA over the closing prices.
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s" % (bar.getClose(), self.__sma[-1]))

# Load the yahoo feed from the CSV file
feed = yahoofeed.Feed()
feed.addBarsFromCSV("orcl", "../tests/data/orcl-2000.csv")

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed, "orcl")
myStrategy.run()
