import datetime

from mooquant import plotter, strategy
from mooquant.feed import csvfeed
from mooquant.tools import quandl


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, quandlFeed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.setUseAdjustedValues(True)
        self.__instrument = instrument

        # It is VERY important to add the the extra feed to the event dispatch loop before
        # running the strategy.
        self.getDispatcher().addSubject(quandlFeed)

        # Subscribe to events from the Quandl feed.
        quandlFeed.getNewValuesEvent().subscribe(self.onQuandlData)

    def onQuandlData(self, dateTime, values):
        self.info(values)

    def onBars(self, bars):
        self.info(bars[self.__instrument].getAdjClose())


def main():
    instruments = ["GORO"]

    # Download GORO bars using WIKI source code.
    feed = quandl.build_feed("WIKI", instruments, 2006, 2012, "./histdata")
    quandlFeed = csvfeed.Feed("Date", "%Y-%m-%d")
    quandlFeed.setDateRange(datetime.datetime(2006, 1, 1), datetime.datetime(2012, 12, 31))
    quandlFeed.addValuesFromCSV("histdata/quandl_gold_2.csv")

    strat = MyStrategy(feed, quandlFeed, instruments[0])
    plter = plotter.StrategyPlotter(strat, True, False, False)

    plter.getOrCreateSubplot("quandl").addDataSeries("USD", quandlFeed["USD"])
    plter.getOrCreateSubplot("quandl").addDataSeries("EUR", quandlFeed["EUR"])
    plter.getOrCreateSubplot("quandl").addDataSeries("GBP", quandlFeed["GBP"])

    strat.run()
    plter.plot()


if __name__ == "__main__":
    main()
