from mooquant.tools import tushare

instruments = ['600016', '600036']
tushare.build_feed(instruments=instruments, fromYear=2007, toYear=2018, storage='histdata/tushare')
