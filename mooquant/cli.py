# -*- coding: utf-8 -*-
"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

	You might be tempted to import things from __main__ later, but that will cause
	problems: the code will get executed twice:

	- When you run `python -m mooquant` python will execute
		``__main__.py`` as a script. That means there won't be any
		``mooquant.__main__`` in ``sys.modules``.
	- When you import __main__ it will get executed again (as a module) because
		there's no ``mooquant.__main__`` in ``sys.modules``.

	Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import json
import logging
import re
import socket
import threading
import time

import click
import coloredlogs
from prettytable import PrettyTable
# from mooquant.tools import tushare, mootdx

@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
		ctx.obj["VERBOSE"] = verbose


@cli.command(help='读取股票行情数据.')
@click.option('-s', '--symbol', default='600001', help='股票代码')
@click.option('-b', '--begin', default='600001', help='股票代码')
@click.option('-e', '--end', default='600001', help='股票代码')
@click.option('-m', '--module', default='tushare', help='下载模块')
@click.option('-t', '--tofile', default='feed.csv', help='输出文件')
def fetch(symbol, module, tofile, begin, end):
	module.download_daily_bars(symbol, begin, end, tofile)


def main():
	cli(obj={})
