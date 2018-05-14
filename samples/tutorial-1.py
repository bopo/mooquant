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
    instruments = ['600016', '600036']
    # Load the yahoo feed from the CSV file
    feed = tushare.build_feed(instruments, 2013, 2018, './tests/data')
    # feed = yahoofeed.Feed()
    # feed.addBarsFromCSV("orcl", "./tests/data/orcl-2000.csv")

    # Evaluate the strategy with the feed's bars.
    strat = MyStrategy(feed, instruments[0])
    strat.run()
