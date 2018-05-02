from mooquant import strategy
from mooquant.barfeed import yahoofeed
from mooquant.technical import ma
from mooquant.technical import rsi


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma = ma.SMA(self.__rsi, 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__rsi[-1], self.__sma[-1]))

if __name__ == '__main__':
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("orcl", "./tests/data/orcl-2000.csv")

    # Evaluate the strategy with the feed's bars.
    strat = MyStrategy(feed, "orcl")
    strat.run()
