#!/bin/sh

export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH=.

tox -v -e py36
tox -v -e py37
