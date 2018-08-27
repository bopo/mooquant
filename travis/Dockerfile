# ARG MOOQUANT_TAG
# FROM gbecedillas/mooquant:${MOOQUANT_TAG}
FROM gbecedillas/mooquant:0.3.3-py37

MAINTAINER BoPo <ibopo@126.com>

RUN apt-get update

RUN pip install tox

RUN apt-get install -y python-tk 

RUN pip freeze

RUN mkdir /tmp/mooquant

COPY setup.py /tmp/mooquant/
COPY travis/run_tests.sh /tmp/mooquant/
COPY coverage.cfg /tmp/mooquant/
COPY tox.ini /tmp/mooquant/
COPY mooquant /tmp/mooquant/mooquant
COPY testcases /tmp/mooquant/testcases
COPY samples /tmp/mooquant/samples

RUN pip uninstall -y mooquant
