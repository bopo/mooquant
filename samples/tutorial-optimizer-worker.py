import rsi2
from mooquant.optimizer import worker

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    worker.run(
        strategyClass=rsi2.RSI2, 
        workerName="localworker",
        address="localhost", 
        drivce='xml',
        port=5000
    )
