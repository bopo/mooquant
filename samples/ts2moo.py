import tushare as ts
import pandas as pd
import click
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
	ctx.obj["VERBOSE"] = verbose


@cli.command(help='读取股票行情数据.')
@click.option('-s', '--symbol', default='600848', help='股票代码')
@click.option('-k', '--ktype', default='D', help='股票代码')
@click.option('-b', '--begin', default=None, help='下载模块')
@click.option('-e', '--end', default=None, help='股票代码')
def fetch(symbol, ktype, begin, end):

	logger.info('starting...')
	# 得到15分钟数据（股票600848,始于2016-01-01,止于2016-05-24,15分钟数据）
	df = ts.get_hist_data(symbol, ktype=ktype)
	# 数据存盘
	# data.to_csv('15-600848.csv')
	# 读出数据，DataFrame格式
	# df = pd.read_csv('15-600848.csv')
	# 从df中选取数据段，改变段名；新段'Adj Close'使用原有段'close'的数据
	logger.info('covering...')

	df2 = pd.DataFrame({'Date Time' : df.index, 'Open' : df['open'],
	                    'High' : df['high'],'Close' : df['close'],
	                    'Low' : df['low'],'Volume' : df['volume'],
	                    'Adj Close':df['close']})

	df2 = df2.sort_index(ascending=True)
	df2 = df2.reset_index(drop=True)

	# 按照Yahoo格式的要求，调整df2各段的顺序
	df2['Date Time'] = pd.to_datetime(df2['Date Time'], format='%Y-%m-%d %H:%M:%S')
	
	dt = df2.pop('Date Time')
	df2.insert(0, 'Date Time', dt)

	op = df2.pop('Open')
	df2.insert(1, 'Open', op)

	high = df2.pop('High')
	df2.insert(2, 'High', high)

	low = df2.pop('Low')
	df2.insert(3, 'Low', low)

	close = df2.pop('Close')
	df2.insert(4, 'Close', close)

	volume = df2.pop('Volume')
	df2.insert(5, 'Volume', volume)

	# 新格式数据存盘，不保存索引编号
	df2.to_csv("%s-%s.csv" % (symbol, ktype), index=False, date_format='%Y-%m-%d %H:%M:%S')

	logger.info("save %s-%s.csv" % (symbol, ktype))

def main():
	cli(obj={})

if __name__ == '__main__':
	main()
