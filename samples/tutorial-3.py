from mooquant import strategy
from mooquant.technical import ma, rsi
from mooquant.tools import tushare


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
    # feed = yahoofeed.Feed()
    # feed.addBarsFromCSV("orcl", "./tests/data/orcl-2000.csv")

    instrument = '600016'
    feed = tushare.build_feed([instrument], 2013, 2018, './tests/data')
    # Evaluate the strategy with the feed's bars.
    strat = MyStrategy(feed, instrument)
    strat.run()
