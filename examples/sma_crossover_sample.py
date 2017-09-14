# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

from mooquant import plotter
from mooquant.stratanalyzer import sharpe
from mooquant.tools import yahoofinance

from sma_crossover import SMACrossOver


def main(plot):
    instrument = "aapl"
    smaPeriod = 163

    # Download the bars.
    feed = yahoofinance.build_feed([instrument], 2011, 2012, "data")

    strat = SMACrossOver(feed, instrument, smaPeriod)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)
        plt.getInstrumentSubplot(instrument).addDataSeries("sma", strat.getSMA())

    strat.run()
    print ("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
