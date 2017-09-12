MooQuant
===========

[![Build Status](https://travis-ci.org/gbeced/mooquant.png?branch=master)](https://travis-ci.org/gbeced/mooquant)
[![Coverage Status](https://coveralls.io/repos/gbeced/mooquant/badge.svg?branch=master)](https://coveralls.io/r/gbeced/mooquant?branch=master)


MooQuant is an **event driven algorithmic trading** Python library. Although the initial focus
was on **backtesting**, **paper trading** is now possible using:

 * [Bitstamp](https://www.bitstamp.net/) for Bitcoins

and **live trading** is now possible using:

 * [Bitstamp](https://www.bitstamp.net/) for Bitcoins

To get started with MooQuant take a look at the [tutorial](http://gbeced.github.io/mooquant/docs/v0.18/html/tutorial.html) and the [full documentation](http://gbeced.github.io/mooquant/docs/v0.18/html/index.html).

Main Features
-------------

 * Event driven.
 * Supports Market, Limit, Stop and StopLimit orders.
 * Supports any type of time-series data in CSV format like Yahoo! Finance, Google Finance, Quandl and NinjaTrader.
 * Bitcoin trading support through [Bitstamp](https://www.bitstamp.net/).
 * Technical indicators and filters like SMA, WMA, EMA, RSI, Bollinger Bands, Hurst exponent and others.
 * Performance metrics like Sharpe ratio and drawdown analysis.
 * Handling Twitter events in realtime.
 * Event profiler.
 * TA-Lib integration.

Installation
------------

MooQuant is developed using Python 2.7 and depends on:

 * [NumPy and SciPy](http://numpy.scipy.org/).
 * [pytz](http://pytz.sourceforge.net/).
 * [dateutil](https://dateutil.readthedocs.org/en/latest/).
 * [requests](http://docs.python-requests.org/en/latest/).
 * [matplotlib](http://matplotlib.sourceforge.net/) for plotting support.
 * [ws4py](https://github.com/Lawouach/WebSocket-for-Python) for Bitstamp support.
 * [tornado](http://www.tornadoweb.org/en/stable/) for Bitstamp support.
 * [tweepy](https://github.com/tweepy/tweepy) for Twitter support.

You can install MooQuant using pip like this:

```
pip install mooquant
```
