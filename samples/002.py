# coding=utf-8
from mooquant import broker, plotter, strategy
from mooquant.analyzer import drawdown, returns, sharpe, trades
from mooquant.bar import Frequency
from mooquant.barfeed.csvfeed import GenericBarFeed
from mooquant.technical import ma


# 1.构建一个策略
class MyStrategy(strategy.BacktestingStrategy):

    def __init__(self, feed, instrument, brk):
        super(MyStrategy, self).__init__(feed, brk)
        self.__position = None
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 150)
        self.__instrument = instrument

        self.getBroker()

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
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def getSMA(self):
        return self.__sma

    def onBars(self, bars):# 每一个数据都会抵达这里，就像becktest中的next

        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        #bar.getTyoicalPrice = (bar.getHigh() + bar.getLow() + bar.getClose())/ 3.0
        bar = bars[self.__instrument]

        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # 开多头.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # 平掉多头头寸.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()

# 2.获得回测数据，官网来源于yahoo，由于墙的关系，我们用本地数据
feed = GenericBarFeed(Frequency.DAY, None, None)
feed.addBarsFromCSV("fd", "./tests/data/30min-bitstampUSD.csv")

# 3.broker setting
# 3.1 commission类设置
commission = broker.backtesting.TradePercentage(0.0001)

# 3.2 fill strategy设置
fill_stra = broker.fillstrategy.DefaultStrategy(volumeLimit=0.1)
slip_stra = broker.slippage.NoSlippage()
fill_stra.setSlippageModel(slip_stra)

# 3.3完善broker类
brk = broker.backtesting.Broker(1000000, feed, commission)
brk.setFillStrategy(fill_stra)

# 4.把策略跑起来
strat = MyStrategy(feed, "fd", brk)

# Attach a returns analyzers to the strategy.
trade = trades.Trades()
strat.attachAnalyzer(trade)

# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(strat)

# Run the strategy.
strat.run()
strat.info("Final portfolio value: $%.2f" % strat.getResult())

print ("total number of trades: ")
print (trade.getCount())

print ("commissions for each trade: ")
print (trade.getCommissionsForAllTrades())

# Plot the strategy.
plt.plot()
