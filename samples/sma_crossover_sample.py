from mooquant import plotter
from mooquant.analyzer import sharpe
from mooquant.tools import tushare
from samples import sma_crossover


def main(plot):
    instrument = "600016"
    smaPeriod = 163

    feed = tushare.build_feed([instrument], 2011, 2012, "./histdata/tushare")
    strat = sma_crossover.SMACrossOver(feed, instrument, smaPeriod)

    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)
        plt.getInstrumentSubplot(instrument).addDataSeries("sma", strat.getSMA())

    strat.run()
    print("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
