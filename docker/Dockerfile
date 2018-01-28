FROM ubuntu:latest
MAINTAINER BoPo Wang <ibopo@126.com>

COPY sources.list /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3-setuptools python3-dev
RUN apt-get install -y python3-pip

RUN apt-get install -y gfortran libopenblas-dev liblapack-dev
RUN apt-get install -y libfreetype6-dev
RUN apt-get install -y pkg-config
RUN apt-get install -y wget

RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install pandas
RUN pip3 install patsy
RUN pip3 install statsmodels
RUN pip3 install matplotlib
RUN pip3 install ws4py
RUN pip3 install tornado
RUN pip3 install tweepy
RUN pip3 install cython

# TA-Lib
RUN cd /tmp; \
	wget http://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz; \
	tar -xzf ta-lib-0.4.0-src.tar.gz; \
	cd ta-lib; \
	./configure ; make; make install; \
	cd ..; \
	rm ta-lib-0.4.0-src.tar.gz; \
	rm -rf ta-lib

RUN pip3 install TA-Lib
RUN pip3 install mooquant==0.2.5
