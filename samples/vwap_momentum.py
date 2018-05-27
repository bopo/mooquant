from mooquant import plotter, strategy
from mooquant.analyzer import sharpe
from mooquant.technical import vwap
from mooquant.tools import tushare


class VWAPMomentum(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, vwapWindowSize, threshold):
        super().__init__(feed)

        self.__instrument = instrument
        self.__vwap = vwap.VWAP(feed[instrument], vwapWindowSize)
        self.__threshold = threshold

    def getVWAP(self):
        return self.__vwap

    def onBars(self, bars):
        vwap = self.__vwap[-1]

        if vwap is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        price = bars[self.__instrument].getClose()
        notional = shares * price

        if price > vwap * (1 + self.__threshold) and notional < 1000000:
            self.marketOrder(self.__instrument, 100)
        elif price < vwap * (1 - self.__threshold) and notional > 0:
            self.marketOrder(self.__instrument, -100)


def main(plot):
    instrument = '600016'
    vwapWindowSize = 5
    threshold = 0.01

    feeds = tushare.build_feed([instrument], 2010, 2018, './histdata/tushare')
    strat = VWAPMomentum(feeds, instrument, vwapWindowSize, threshold)

    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    plter = plotter.StrategyPlotter(strat, True, False, True)
    plter.getInstrumentSubplot(instrument).addDataSeries("vwap", strat.getVWAP())

    strat.run()

    strat.info("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))
    plter.plot()


if __name__ == "__main__":
    main(True)
