optimizer -- Parallel optimizers
================================

.. automodule:: mooquant.optimizer.server
    :members:
    :member-order: bysource
    :show-inheritance:

.. automodule:: mooquant.optimizer.worker
    :members:
    :member-order: bysource
    :show-inheritance:

.. automodule:: mooquant.optimizer.local
    :members:
    :member-order: bysource
    :show-inheritance:

.. note::
    * The server component will split strategy executions in chunks which are distributed among the different workers. **mooquant.optimizer.server.Server.defaultBatchSize** controls the chunk size.
    * The :meth:`mooquant.strategy.BaseStrategy.getResult` method is used to select the best strategy execution. You can override that method to rank executions using a different criteria.

