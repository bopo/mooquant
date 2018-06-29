from mooquant.optimizer import worker

from samples import rsi2

if __name__ == '__main__':
    worker.run(
        strategyClass=rsi2.RSI2,
        workerName="localworker",
        address="127.0.0.1",
        drivce='zmq',
        port=5000
    )
