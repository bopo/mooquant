from mooquant import plotter
from mooquant.analyzer import returns
from mooquant.tools import tushare
from samples import sma_crossover

if __name__ == '__main__':
    instrument = '600016'

    feeds = tushare.build_feed([instrument], 2016, 2018, './histdata/tushare')
    strat = sma_crossover.SMACrossOver(feeds, instrument, 20)

    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)

    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(strat)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot("orcl").addDataSeries("SMA", strat.getSMA())
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    # Run the strategy.
    strat.run()
    strat.info("Final portfolio value: $%.2f" % strat.getResult())

    # Plot the strategy.
    plt.plot()
