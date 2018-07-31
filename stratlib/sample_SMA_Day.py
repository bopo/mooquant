from mooquant import plotter, strategy
from mooquant.analyzer import drawdown, returns, sharpe, trades
from mooquant.broker.backtesting import TradePercentage
from mooquant.broker.fillstrategy import DefaultStrategy
from mooquant.technical import cross, ma
from mooquant.tools import tushare


class thrSMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, short_l, mid_l, long_l, up_cum):
        strategy.BacktestingStrategy.__init__(self, feed)

        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.001))

        self.__position = None
        self.__instrument = instrument
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__malength1 = int(short_l)
        self.__malength2 = int(mid_l)
        self.__malength3 = int(long_l)
        self.__circ = int(up_cum)

        self.__ma1 = ma.SMA(self.__prices, self.__malength1)
        self.__ma2 = ma.SMA(self.__prices, self.__malength2)
        self.__ma3 = ma.SMA(self.__prices, self.__malength3)

        self.__datetime = feed[instrument].getDateTimes()
        self.__open = feed[instrument].getOpenDataSeries()
        self.__high = feed[instrument].getHighDataSeries()
        self.__low = feed[instrument].getLowDataSeries()
        self.__close = feed[instrument].getCloseDataSeries()

    def getPrice(self):
        return self.__prices

    def getSMA(self):
        return self.__ma1, self.__ma2, self.__ma3

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOK(self):
        pass

    def onExitOk(self, position):
        self.__position = None
        # self.info("long close")

    def onExitCanceled(self, position):
        self.__position.exitMarket()

    def buyCon1(self):
        if cross.cross_above(self.__ma1, self.__ma2) > 0:
            return True

    def buyCon2(self):
        m1 = 0
        m2 = 0
        
        for i in range(self.__circ):
            if self.__ma1[-i - 1] > self.__ma3[-i - 1]:
                m1 += 1

            if self.__ma2[-i - 1] > self.__ma3[-i - 1]:
                m2 += 1

        if m1 >= self.__circ and m2 >= self.__circ:
            return True

    def sellCon1(self):
        if cross.cross_below(self.__ma1, self.__ma2) > 0:
            return True

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long
        # position.
        self.dayInfo(bars[self.__instrument])

        if self.__ma2[-1] is None:
            return

        if self.__position is not None:
            if not self.__position.exitActive() and cross.cross_below(
                    self.__ma1, self.__ma2) > 0:
                self.__position.exitMarket()
                # self.info("sell %s" % (bars.getDateTime()))

        if self.__position is None:
            if self.buyCon1() and self.buyCon2():
                shares = int(self.getBroker().getCash() * 0.2 /
                             bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares)

    def dayInfo(self, bar):
        try:
            self.__openD[-1]
        except AttributeError:
            self.__openD = []
            self.__highD = []
            self.__lowD = []
            self.__closeD = []
            self.__upper_limit = []
            self.__lower_limit = []

        if len(self.__datetime) < 2:
            self.__openD.append(bar.getOpen())
            self.__highD.append(self.__high[-1])
            self.__lowD.append(self.__low[-1])
            self.__closeD.append(self.__close[-1])
            
            return

        # if another day
        if self.__datetime[-1].date() != self.__datetime[-2].date():
            self.__openD.append(bar.getOpen())
            self.__highD.append(self.__high[-1])
            self.__lowD.append(self.__low[-1])
            self.__closeD.append(self.__close[-1])

            self.__upper_limit.append(
                round(round(self.__closeD[-2] * 1.1 * 1000) / 10) / 100)

            self.__lower_limit.append(
                round(round(self.__closeD[-2] * 0.9 * 1000) / 10) / 100)

            print(self.__datetime[-1].date(),
                  self.__datetime[-2].date(), self.__openD[-1])

        elif self.__datetime[-1].date() == self.__datetime[-2].date():
            if self.__high[-1] > self.__highD[-1]:
                self.__highD[-1] = self.__high[-1]

            if self.__low[-1] < self.__lowD[-1]:
                self.__lowD[-1] = self.__low[-1]

            self.__closeD[-1] = self.__close[-1]


def main():
    strat = thrSMA
    instrument = '600288'
    paras = [2, 20, 60, 10]

    feeds = tushare.build_feed([instrument], 2016, 2017, "histdata/tushare")
    strat = strat(feeds, instrument, *paras)

    retAnalyzer = returns.Returns()
    strat.attachAnalyzer(retAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradesAnalyzer)

    plter = plotter.StrategyPlotter(strat, True, True, True)
    strat.run()
    plter.plot()

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


if __name__ == "__main__":
    main()
