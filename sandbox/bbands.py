from mooquant import plotter, strategy
from mooquant.analyzer import sharpe
from mooquant.technical import bollinger
from mooquant.tools import tushare


class BBandsStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bBandsPeriod):
        super().__init__(feed)

        self.__instrument = instrument
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)

    def getBollingerBands(self):
        return self.__bbands

    def onBars(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]

        if lower is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]

        if shares == 0 and bar.getClose() < lower:
            sharesToBuy = int(self.getBroker().getCash(False) / bar.getClose())
            self.marketOrder(self.__instrument, sharesToBuy)
        elif shares > 0 and bar.getClose() > upper:
            self.marketOrder(self.__instrument, -1 * shares)


def main(plot=False):
    instruments = ["600036"]
    bBandsPeriod = 20

    feeds = tushare.build_feed(instruments, 2017, 2018, "./tests/data")
    strat = BBandsStrategy(feeds, instruments[0], bBandsPeriod)
    sharp = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharp)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, True, True)
        plt.getInstrumentSubplot(instruments[0]).addDataSeries("upper", strat.getBollingerBands().getUpperBand())
        plt.getInstrumentSubplot(instruments[0]).addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
        plt.getInstrumentSubplot(instruments[0]).addDataSeries("lower", strat.getBollingerBands().getLowerBand())

    strat.run()

    print("Sharpe ratio: %.2f" % sharp.getSharpeRatio(0.05))

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
