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

    instrument = '600016'
    feeds = tushare.build_feed([instrument], 2016, 2018, './histdata/tushare')

    # Evaluate the strategy with the feed's bars.
    strat = MyStrategy(feeds, instrument)
    strat.run()
