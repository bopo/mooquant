# MooQuant
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import pickle
import threading
import time

import zerorpc

import mooquant.logger
from mooquant.optimizer import base

logger = mooquant.logger.getLogger(__name__)


class Job(object):
    def __init__(self, strategyParameters):
        self.__strategyParameters = strategyParameters
        self.__bestResult = None
        self.__bestParameters = None
        self.__id = id(self)

    def getId(self):
        return self.__id

    def getNextParameters(self):
        ret = None
        
        if len(self.__strategyParameters):
            ret = self.__strategyParameters.pop()
        
        return ret


class RPCService(object):
    defaultBatchSize = 200

    def __init__(self, paramSource, resultSinc, barFeed):
        self.__paramSource = paramSource
        self.__resultSinc = resultSinc
        self.__barFeed = barFeed
        self.__instrumentsAndBars = None  # Pickle'd instruments and bars for faster retrieval.
        self.__barsFreq = None
        self.__activeJobs = {}
        self.__activeJobsLock = threading.Lock()
        self.__forcedStop = False
        self.__bestResult = None

        self.serve()

    def getInstrumentsAndBars(self):
        return self.__instrumentsAndBars

    def getBarsFrequency(self):
        return str(self.__barsFreq)

    def getNextJob(self):
        ret = None

        # Get the next set of parameters.
        params = self.__paramSource.getNext(self.defaultBatchSize)
        params = [p.args for p in params]

        # Map the active job
        if len(params):
            ret = Job(params)
            
            with self.__activeJobsLock:
                self.__activeJobs[ret.getId()] = ret

        return pickle.dumps(ret)

    def jobsPending(self):
        if self.__forcedStop:
            return False

        jobsPending = not self.__paramSource.eof()

        with self.__activeJobsLock:
            activeJobs = len(self.__activeJobs) > 0

        return jobsPending or activeJobs

    def pushJobResults(self, jobId, result, parameters, workerName):
        jobId = pickle.loads(jobId)
        result = pickle.loads(result)
        parameters = pickle.loads(parameters)

        # Remove the job mapping.
        with self.__activeJobsLock:
            try:
                del self.__activeJobs[jobId]
            except KeyError:
                # The job's results were already submitted.
                return

        # if result is None or result > self.__bestResult:
        
        if result is None:
            logger.info("Best result so far %s with parameters %s" % (result, parameters))
            self.__bestResult = result
        elif self.__bestResult is None and result is not None:
            logger.info("Best result so far %s with parameters %s" % (result, parameters))
            self.__bestResult = result            
        elif result > self.__bestResult:
            logger.info("Best result so far %s with parameters %s" % (result, parameters))
            self.__bestResult = result

        self.__resultSinc.push(result, base.Parameters(*parameters))

    def serve(self):
        try:
            # Initialize instruments, bars and parameters.
            logger.info("Loading bars")
            loadedBars = []
            
            for dateTime, bars in self.__barFeed:
                loadedBars.append(bars)
            
            instruments = self.__barFeed.getRegisteredInstruments()

            self.__instrumentsAndBars = pickle.dumps((list(instruments), loadedBars))
            self.__barsFreq = self.__barFeed.getFrequency()
        finally:
            pass

class Server(object):

    def __init__(self, paramSource, resultSinc, barFeed, address, port, autoStop=True):
        self.__zerorpc = zerorpc.Server(RPCService(paramSource, resultSinc, barFeed))
        self.__zerorpc.bind("tcp://%s:%s" % (address, port))

    def stop(self):
        pass

    def serve(self):
        logger.info("Waiting for workers")
        self.__zerorpc.run()
