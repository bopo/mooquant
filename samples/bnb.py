from binance.client import Client

apikey = 'w9j8X6B4c6RC2WaqoO9eud0Ev7RKbxw6ioBekRoeVnu3DAHqy9mqer9ktaYkN7GR'
serect = 'uWsFyaUiGzdvfwqhIMoji0wR39sUXg3aHmrSgHfU1CtQXbWEwifnk4cIbOpa3SZ7'

client = Client(apikey, serect)

# get market depth
depth = client.get_order_book(symbol='BNBBTC')

# place market buy order
# order = client.create_order(
#     symbol='BNBBTC', 
#     side=Client.SIDE_BUY, 
#     type=Client.ORDER_TYPE_MARKET, 
#     quantity=100)

# get all symbol prices
prices = client.get_all_tickers()

# withdraw 100 ETH
# check docs for assumptions around withdrawals
# from binance.exceptions import BinanceApiException, BinanceWithdrawException

# try:
#     result = client.withdraw(
#         asset='ETH',
#         address='<eth_address>',
#         amount=100)
# except BinanceApiException as e:
#     print(e)
# except BinanceWithdrawException as e:
#     print(e)
# else:
#     print("Success")

# fetch list of withdrawals
# withdraws = client.get_withdraw_history()

# fetch list of ETH withdrawals
# eth_withdraws = client.get_withdraw_history('ETH')

# get a deposit address
# address = client.get_deposit_address('BTC')

# start trade websocket
def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)
    # do something

from binance.websockets import BinanceSocketManager
bm = BinanceSocketManager(client)
bm.start_aggtrade_socket(symbol='BNBBTC', callback=process_message)
bm.start()