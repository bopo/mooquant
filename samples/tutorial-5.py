from mooquant import plotter
from mooquant.barfeed import yahoofeed
from mooquant.analyzer import returns

import sma_crossover

if __name__ == '__main__':
	# Load the yahoo feed from the CSV file
	feed = yahoofeed.Feed()
	feed.addBarsFromCSV("orcl", "./tests/data/orcl-2000.csv")

	# Evaluate the strategy with the feed's bars.
	strat = sma_crossover.SMACrossOver(feed, "orcl", 20)

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
