from mooquant import plotter, strategy
from mooquant.analyzer import drawdown, returns, sharpe, trades
from mooquant.broker.backtesting import TradePercentage
from mooquant.broker.fillstrategy import DefaultStrategy
from mooquant.technical import cross, ma


class DMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, n, m):
        strategy.BacktestingStrategy.__init__(self, feed)

        self.__instrument = instrument

        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.001))

        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__malength1 = int(n)
        self.__malength2 = int(m)

        self.__ma1 = ma.SMA(self.__prices, self.__malength1)
        self.__ma2 = ma.SMA(self.__prices, self.__malength2)

    def getPrice(self):
        return self.__prices

    def getSMA(self):
        return self.__ma1, self.__ma2

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOK(self):
        pass

    def onExitOk(self, position):
        self.__position = None
        # self.info("long close")

    def onExitCanceled(self, position):
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long
        # position.

        if self.__ma2[-1] is None:
            return

        if self.__position is not None:
            if not self.__position.exitActive() and cross.cross_below(
                    self.__ma1, self.__ma2) > 0:
                self.__position.exitMarket()
                # self.info("sell %s" % (bars.getDateTime()))

        if self.__position is None:
            if cross.cross_above(self.__ma1, self.__ma2) > 0:
                shares = int(self.getBroker().getEquity() * 0.2 /
                             bars[self.__instrument].getPrice())

                self.__position = self.enterLong(self.__instrument, shares)

                print(bars[self.__instrument].getDateTime(),
                      bars[self.__instrument].getPrice())


def testStrategy():
    instrument = '600288'
    fromDate = '20150101'
    toDate = '20150601'
    paras = [5, 20]
    strat = DMA
    plot = True

    from mooquant.tools import tushare
    feeds = tushare.build_feed([instrument], 2015, 2016, "histdata/tushare")
    strat = strat(feeds, instrument, *paras)

    retAnalyzer = returns.Returns()
    strat.attachAnalyzer(retAnalyzer)

    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    drawDownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawDownAnalyzer)

    tradesAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradesAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, True, True)

    strat.run()

    # 夏普率
    sharp = sharpeRatioAnalyzer.getSharpeRatio(0.05)

    # 最大回撤
    maxdd = drawDownAnalyzer.getMaxDrawDown()

    # 收益率
    return_ = retAnalyzer.getCumulativeReturns()[-1]

    # 收益曲线
    return_list = []

    for item in retAnalyzer.getCumulativeReturns():
        return_list.append(item)

    if plot:
        plt.plot()


if __name__ == "__main__":
    testStrategy()
