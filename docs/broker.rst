broker -- Order management classes
==================================

Base module and classes
------------------------

.. automodule:: mooquant.broker
    :members: Order, MarketOrder, LimitOrder, StopOrder, StopLimitOrder, OrderExecutionInfo, Broker
    :member-order: bysource
    :show-inheritance:

Backtesting module and classes
------------------------------

.. automodule:: mooquant.broker.backtesting
    :members: Commission, NoCommission, FixedPerTrade, TradePercentage, Broker
    :show-inheritance:

.. automodule:: mooquant.broker.slippage
    :members: SlippageModel, NoSlippage, VolumeShareSlippage
    :show-inheritance:

.. automodule:: mooquant.broker.fillstrategy
    :members: FillStrategy, DefaultStrategy
    :show-inheritance:
