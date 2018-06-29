from mooquant.optimizer import worker

from rsi2 import RSI2

if __name__ == '__main__':
    worker.run(
        strategyClass=RSI2,
        workerName="worker",
        address="127.0.0.1",
        drivce='zmq',
        port=5000
    )
