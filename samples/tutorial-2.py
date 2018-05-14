from mooquant import strategy
from mooquant.technical import ma
from mooquant.tools import tushare


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super().__init__(feed)
        # We want a 15 period SMA over the closing prices.
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s" % (bar.getClose(), self.__sma[-1]))


if __name__ == '__main__':
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()
    # feed.addBarsFromCSV("orcl", "./tests/data/orcl-2000.csv")
    instrument = '600016'
    feed = tushare.build_feed([instrument], 2013, 2018, './tests/data')

    # Evaluate the strategy with the feed's bars.
    strat = MyStrategy(feed, instrument)
    strat.run()
