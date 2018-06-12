from mooquant.tools import mootdx

instruments = ['600016', '600036']
mootdx.build_feed(instruments=instruments, fromYear=2007, toYear=2018, storage='histdata')
