# coding=utf-8
from mooquant import strategy
from mooquant.analyzer import returns, sharpe
from mooquant.bar import Frequency
from mooquant.barfeed.csvfeed import GenericBarFeed
from mooquant.utils import stats


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed):
        super(MyStrategy, self).__init__(feed, 10000000)
        self.__position = None

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at %.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        self.__position.exitMarket()

    def onBars(self, bars):
        # 1.我们弄一个简单的策略来假装一下
        day = bars.getDateTime().date().day
        if day == 5:
            self.__position = self.enterLong('a', 1, True)
        elif day == 10:
            self.__position = self.enterLong('b', 1, True)
        elif day == 15:
            self.__position = self.enterLong('c', 1, True)
        elif day == 20:
            self.__position = self.enterLong('d', 1, True)

# 2.读取csv文件.
feed = GenericBarFeed(Frequency.DAY, None, None)
feed.addBarsFromCSV("a", "a.csv")
feed.addBarsFromCSV("b", "b.csv")
feed.addBarsFromCSV("c", "c.csv")
feed.addBarsFromCSV("d", "d.csv")

strat = MyStrategy(feed)

# 3.加入分析器
retAnalyzer = returns.Returns()
strat.attachAnalyzer(retAnalyzer)
sharpeRatioAnalyzer = sharpe.SharpeRatio()
strat.attachAnalyzer(sharpeRatioAnalyzer)

# 4.运行策略
strat.run()

# 5.输出结果

# 最终的投资组合价值
print("Final portfolio value: $%.2f" % strat.getResult())

# 年化平均收益率
print("Anual return: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))

# 平均日收益
print("Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100))

# 每日收益标准开发
print("Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns())))

# 夏普比率
print("Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0)))
