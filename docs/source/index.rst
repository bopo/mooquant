
===============================
MooQuant |version| Documentation
===============================

..  image:: https://img.shields.io/travis/mooquant/mooquant/master.svg
    :target: https://travis-ci.org/mooquant/mooquant/branches
    :alt: Build

..  image:: https://coveralls.io/repos/github/mooquant/mooquant/badge.svg?branch=master
    :target: https://coveralls.io/github/mooquant/mooquant?branch=master

..  image:: https://readthedocs.org/projects/mooquant/badge/?version=stable
    :target: http://mooquant.readthedocs.io/zh_CN/stable/?badge=stable
    :alt: Documentation Status

..  image:: https://img.shields.io/pypi/v/mooquant.svg
    :target: https://pypi.python.org/pypi/mooquant
    :alt: PyPI Version

..  image:: https://img.shields.io/pypi/l/mooquant.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License

..  image:: https://img.shields.io/pypi/pyversions/mooquant.svg
    :target: https://pypi.python.org/pypi/mooquant
    :alt: Python Version Support


MooQuant 从数据获取、算法交易、回测引擎，实盘模拟，实盘交易到数据分析，为程序化交易者提供了全套解决方案。

MooQuant 具有灵活的配置方式，强大的扩展性，用户可以非常容易地定制专属于自己的程序化交易系统。

.. note::

    MooQuant 所有的策略都可以直接在 `MooQuant`_ 上进行回测和实盘模拟，并且可以通过微信和邮件实时推送您的交易信号。`MooQuant`_ 是一个开放的量化算法交易社区，为程序化交易者提供免费的回测和实盘模拟环境，并且会不间断举行实盘资金投入的量化比赛。

特点
============================

======================    =================================================================================
易于使用                    让您集中于策略的开发，一行简单的命令就可以执行您的策略。
完善的文档                   您可以直接访问 `MooQuant 文档`_ 或者 `MooQuant 文档`_ 来获取您需要的信息。
活跃的社区                   您可以通过访问 `MooQuant 社区`_ 获取和询问有关 MooQuant 的一切问题，有很多优秀的童鞋会解答您的问题。
稳定的环境                   每天都有会大量的算法交易在 MooQuant上运行，无论是 MooQuant，还是数据，我们能会做到问题秒处理，秒解决。
灵活的配置                   您可以使用多种方式来配置和运行策略，只需简单的配置就可以构建适合自己的交易系统。
强大的扩展性                 开发者可以基于我们提供的 Mod Hook 接口来进行扩展。
======================    =================================================================================


.. note::

    如果您基于 MooQuant 进行了 Mod 扩展，欢迎告知我们。在审核通过后，会在 Mod 列表中添加相关信息。


获取帮助
============================

关于 MooQuant 的任何问题可以通过以下途径来获取帮助

*  可以通过 `索引`_ 或者使用搜索功能来查找特定问题
*  在 `Github Issue`_ 中提交issue
*  MooQuant 交流群「162849769」


.. _Github Issue: https://github.com/bopo/mooquant/issues
.. _MooQuant: https://www.mooquant.com/algorithms
.. _MooQuant 文档: http://mooquant.readthedocs.io/zh_CN/latest/
.. _MooQuant 社区: https://www.mooquant.com/community/category/all/
.. _FAQ: http://mooquant.readthedocs.io/zh_CN/latest/faq.html
.. _索引: http://mooquant.readthedocs.io/zh_CN/latest/genindex.html

.. _MooQuant 介绍: http://mooquant.readthedocs.io/zh_CN/latest/intro/overview.html
.. _安装指南: http://mooquant.readthedocs.io/zh_CN/latest/intro/install.html
.. _10分钟学会 MooQuant: http://mooquant.readthedocs.io/zh_CN/latest/intro/tutorial.html
.. _策略示例: http://mooquant.readthedocs.io/zh_CN/latest/intro/examples.html

.. _API: http://mooquant.readthedocs.io/zh_CN/latest/api/base_api.html

.. _如何贡献代码: http://mooquant.readthedocs.io/zh_CN/latest/development/make_contribute.html
.. _基本概念: http://mooquant.readthedocs.io/zh_CN/latest/development/basic_concept.html
.. _MooQuant 基于 Mod 进行扩展: http://mooquant.readthedocs.io/zh_CN/latest/development/mod.html
.. _History: http://mooquant.readthedocs.io/zh_CN/latest/history.html
.. _TODO: https://github.com/mooquant/mooquant/blob/master/TODO.md
.. _develop 分支: https://github.com/mooquant/mooquant/tree/develop
.. _master 分支: https://github.com/mooquant/mooquant
.. _mooquant_mod_sys_stock_realtime: https://github.com/mooquant/mooquant/blob/master/mooquant/mod/mooquant_mod_sys_stock_realtime/README.rst
.. _mooquant_mod_tushare: https://github.com/mooquant/mooquant-mod-tushare
.. _通过 Mod 扩展 MooQuant: http://mooquant.io/zh_CN/latest/development/mod.html
.. _sys_analyser: https://github.com/mooquant/mooquant/blob/master/mooquant/mod/mooquant_mod_sys_analyser/README.rst
.. _sys_funcat: https://github.com/mooquant/mooquant/blob/master/mooquant/mod/mooquant_mod_sys_funcat/README.rst
.. _sys_progress: https://github.com/mooquant/mooquant/blob/master/mooquant/mod/mooquant_mod_sys_progress/README.rst
.. _sys_risk: https://github.com/mooquant/mooquant/blob/master/mooquant/mod/mooquant_mod_sys_risk/README.rst
.. _sys_simulation: https://github.com/mooquant/mooquant/blob/master/mooquant/mod/mooquant_mod_sys_simulation/README.rst
.. _sys_stock_realtime: https://github.com/mooquant/mooquant/blob/master/mooquant/mod/mooquant_mod_sys_stock_realtime/README.rst
.. _vnpy: https://github.com/mooquant/mooquant-mod-vnpy
.. _sentry: https://github.com/mooquant/mooquant-mod-sentry
.. _tushare: https://github.com/mooquant/mooquant-mod-tushare
.. _shipane: https://github.com/wh1100717/mooquant-mod-ShiPanE

.. include:: menus.rst