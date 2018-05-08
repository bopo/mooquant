from mooquant.tools import tushare

tushare.build_feed(instruments=['600016'], fromYear=2017, toYear=2018, storage='tushare')
