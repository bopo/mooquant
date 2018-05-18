项目简介
============

MooQuant 是一个基于事件驱动的 Python 算法交易库，它支持:
 * 基于CSV文件里的历史数据进行回测.
 * 基于 :ref:`Bitstamp <bitstamp-tutorial-label>` 的实时数据进行模拟交易.
 * 基于Bitstamp平台进行真实交易.

It should also make it easy to optimize a strategy using multiple computers.

MooQuant is developed using Python 2.7 and depends on:
 * NumPy and SciPy (http://numpy.scipy.org/).
 * pytz (http://pytz.sourceforge.net/).
 * matplotlib (http://matplotlib.sourceforge.net/) for plotting support.
 * ws4py (https://github.com/Lawouach/WebSocket-for-Python) for Bitstamp support.
 * tornado (http://www.tornadoweb.org/en/stable/) for Bitstamp support.
 * tweepy (https://github.com/tweepy/tweepy) for Twitter support.

so you need to have those installed in order to use this library.

You can install MooQuant using pip like this: ::

    pip install mooquant

