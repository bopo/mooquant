from mooquant.optimizer import worker

from rsi2 import RSI2

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    worker.run(
        strategyClass=RSI2,
        workerName="worker",
        address="localhost",
        drivce='xml',
        port=5000
    )
