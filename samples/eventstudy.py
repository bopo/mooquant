from mooquant import eventprofiler
from mooquant.barfeed import yahoofeed
from mooquant.technical import ma, roc, stats


class BuyOnGap(eventprofiler.Predicate):
    def __init__(self, feed):
        super().__init__()

        stdDevPeriod = 90
        smaPeriod = 20

        self.__returns = {}
        self.__stdDev = {}
        self.__ma = {}

        for instrument in feed.getRegisteredInstruments():
            priceDS = feed[instrument].getAdjCloseDataSeries()
            # Returns over the adjusted close values.
            self.__returns[instrument] = roc.RateOfChange(priceDS, 1)
            # StdDev over those returns.
            self.__stdDev[instrument] = stats.StdDev(self.__returns[instrument], stdDevPeriod)
            # MA over the adjusted close values.
            self.__ma[instrument] = ma.SMA(priceDS, smaPeriod)

    def __gappedDown(self, instrument, bards):
        ret = False

        if self.__stdDev[instrument][-1] is not None:
            prevBar = bards[-2]
            currBar = bards[-1]
            low2OpenRet = (currBar.getOpen(True) - prevBar.getLow(True)) / float(prevBar.getLow(True))

            if low2OpenRet < (self.__returns[instrument][-1] - self.__stdDev[instrument][-1]):
                ret = True

        return ret

    def __aboveSMA(self, instrument, bards):
        ret = False

        if self.__ma[instrument][-1] is not None and bards[-1].getOpen(True) > self.__ma[instrument][-1]:
            ret = True

        return ret

    def eventOccurred(self, instrument, bards):
        ret = False

        if self.__gappedDown(instrument, bards) and self.__aboveSMA(instrument, bards):
            ret = True

        return ret


def main(plot):
    instruments = ["orcl", ]

    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instruments[0], "./tests/data/orcl-2000.csv")

    predicate = BuyOnGap(feed)
    eventProfiler = eventprofiler.Profiler(predicate, 5, 5)
    eventProfiler.run(feed, True)

    results = eventProfiler.getResults()
    print("%d events found" % (results.getEventCount()))

    if plot:
        eventprofiler.plot(results)


if __name__ == "__main__":
    main(True)
