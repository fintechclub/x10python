from binance.websockets import BinanceSocketManager
from binance.client import Client
import json
import pprint

sellOrders = {}
buyOrders = {}
def process_message(msg):
    #print("message type: {}".format(msg['e']))
    
    #if not msg['m']:        
    #else     
    print(msg)
    
    
    

client = Client("api_key", "api_secret")

bm = BinanceSocketManager(client)
# start any sockets here, i.e a trade socket
conn_key = bm.start_trade_socket('BTCUSDT', process_message)
# then start the socket manager
bm.start()


