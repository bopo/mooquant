import itertools

from mooquant.optimizer import local
from mooquant.tools import tushare

from samples import rsi2


def parameters_generator(instrument):
    entrySMA = list(range(150, 251))
    exitSMA = list(range(5, 16))
    rsiPeriod = list(range(2, 11))
    overBoughtThreshold = list(range(75, 96))
    overSoldThreshold = list(range(5, 26))
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)


if __name__ == '__main__':
    instruments = ['600016']
    
    feeds = tushare.build_feed(instruments, 2016, 2018, './histdata/tushare')
    local.run(rsi2.RSI2, feeds, parameters_generator(instruments))
