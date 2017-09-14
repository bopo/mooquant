# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import rsi2
from mooquant.optimizer import worker

if __name__ == '__main__':
    worker.run(rsi2.RSI2, "localhost", 5000, workerName="localworker")
