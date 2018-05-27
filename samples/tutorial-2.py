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

    instrument = '600016'
    feeds = tushare.build_feed([instrument], 2016, 2018, './histdata/tushare')

    # Evaluate the strategy with the feed's bars.
    strat = MyStrategy(feeds, instrument)
    strat.run()
