from mooquant import strategy
from mooquant.tools import tushare

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super().__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())


if __name__ == '__main__':
    instrument = '600036'
    feeds = tushare.build_feed([instrument], 2016, 2018, './histdata/tushare')

    # Evaluate the strategy with the feed's bars.
    strat = MyStrategy(feeds, instrument)
    strat.run()
