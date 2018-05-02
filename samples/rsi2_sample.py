import rsi2
from mooquant import plotter
from mooquant.analyzer import sharpe
from mooquant.barfeed import yahoofeed

def main(plot):
    instrument = "dia"
    entrySMA = 152
    exitSMA = 11
    rsiPeriod = 2
    overBoughtThreshold = 92
    overSoldThreshold = 18

    # Download the bars.
    # feed = quandl.build_feed("WIKI", [instrument], 2009, 2012, "./data")
    feeds = yahoofeed.Feed()
    feeds.addBarsFromCSV("dia", "../tests/data/DIA-2009-yahoofinance.csv")
    feeds.addBarsFromCSV("dia", "../tests/data/DIA-2010-yahoofinance.csv")
    feeds.addBarsFromCSV("dia", "../tests/data/DIA-2011-yahoofinance.csv")

    strat = rsi2.RSI2(feeds, instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)
        plt.getInstrumentSubplot(instrument).addDataSeries("Entry SMA", strat.getEntrySMA())
        plt.getInstrumentSubplot(instrument).addDataSeries("Exit SMA", strat.getExitSMA())
        plt.getOrCreateSubplot("rsi").addDataSeries("RSI", strat.getRSI())
        plt.getOrCreateSubplot("rsi").addLine("Overbought", overBoughtThreshold)
        plt.getOrCreateSubplot("rsi").addLine("Oversold", overSoldThreshold)

    strat.run()
    print("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
