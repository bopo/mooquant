# coding=utf-8
import coloredlogs

from mooquant import plotter, strategy
from mooquant.analyzer import drawdown, sharpe, trades
from mooquant.bar import Frequency
from mooquant.barfeed.csvfeed import GenericBarFeed
from mooquant.technical import ma


# 1.构建一个策略
class Strategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super().__init__(feed)
        self.__position = None
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 150)
        self.__instrument = instrument
        self.getBroker()

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("买入 %.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("卖出 %.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def getSMA(self):
        return self.__sma

    def onBars(self, bars):
        # 每一个数据都会抵达这里，就像becktest中的next
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        # bar.getTyoicalPrice = (bar.getHigh() + bar.getLow() + bar.getClose())/ 3.0
        bar = bars[self.__instrument]

        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # 开多头.
                self.__position = self.enterLong(self.__instrument, 100, True)

        # 平掉多头头寸.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def main():
    import sys
    feeds = GenericBarFeed(Frequency.DAY, None, None)
    feeds.addBarsFromCSV("feeds", sys.argv[1])

    # 3.实例化策略
    strat = Strategy(feeds, "feeds")

    # 4.设置指标和绘图
    ratio = sharpe.SharpeRatio()
    strat.attachAnalyzer(ratio)
    # plter = plotter.StrategyPlotter(strat)

    # 4.设置指标和绘图
    draws = drawdown.DrawDown()
    strat.attachAnalyzer(draws)

    tradeAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradeAnalyzer)

    plter = plotter.StrategyPlotter(strat)
    coloredlogs.install(level='DEBUG')

    # 5.运行策略
    strat.run()
    strat.info("最终收益: %.2f" % strat.getResult())

    # 6.输出夏普率、绘图
    strat.info("夏普比率: " + str(ratio.getSharpeRatio(0)))
    strat.info("最大回撤: " + str(draws.getMaxDrawDown()))
    strat.info("回撤时间: " + str(draws.getLongestDrawDownDuration()))
    plter.plot()


if __name__ == '__main__':
    main()
