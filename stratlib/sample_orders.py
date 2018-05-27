# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 13:06:56 2015

@author: Eunice
"""

from mooquant import bar, plotter, strategy
from mooquant.analyzer import drawdown, returns, sharpe, trades
from mooquant.broker.backtesting import TradePercentage
from mooquant.broker.fillstrategy import DefaultStrategy
from mooquant.technical import ma


class OrderBook(strategy.BacktestingStrategy):
    '''
    头寸设置
    '''
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
        bar = bars[self.__instrument]
        print(bar.getDateTime(), bar.getBp(), bar.getAp())


def testStrategy():
    instrument = '600288'
    frequency = bar.Frequency.TRADE
    fromDate = '20160815'
    toDate = '20160820'
    strat = OrderBook

    paras = [5, 20]
    plot = True

    from mooquant.tools import tushare
    feeds = tushare.build_feed([instrument], 2016, 2017, "tushare")
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

    if plot:
        plt.plot()

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
    testStrategy()
