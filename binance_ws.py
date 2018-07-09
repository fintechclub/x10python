from binance.websockets import BinanceSocketManager
from binance.client import Client
import json
import pprint
import time
import datetime



def callback(msg):
    global last_time
    global sellOrders
    global buyOrders
    global last_price
    global total_data
    q = float(msg['q'])
    
    if last_price == 0:
        last_price = float(msg['p'])
        total_data["first_price"] = last_price
        
    if not msg['m']:   # Buyer     
        order_b = msg['b']    
        if order_b in buyOrders:
            buyOrders[order_b] = tuple(map(lambda x, y: x + y, buyOrders[order_b], (q, 0)))
        else:
            buyOrders[order_b] = (q, 1)
    else:    # Seller     
        order_s = msg['a']
        if order_s in sellOrders:
            sellOrders[order_s] = tuple(map(lambda x, y: x + y, sellOrders[order_s], (q, 0)))
        else:
            sellOrders[order_s] = (q, 1)   
    
    cur_time = int(msg['E'])
    cur_price = float(msg['p'])
    
    if cur_time - last_time > time_frame_sec * 1000:
        utc_time = time.localtime(msg['E']/1000)
        str_cur_time = time.strftime("%Y-%m-%d %H:%M:%S", utc_time)
        
        print("----------TimeFrame = {0:d}, Current time = {1:s} Current price = {2:.2f}, Change price in frame, % = {3:.2%} ------------------------".format(time_frame_sec, 
                    str_cur_time,
                    cur_price,
                    cur_price / last_price - 1))
        
        order_buy_in_tf   = sum(x[1] for x in buyOrders.values())
        order_sell_in_tf  = sum(x[1] for x in sellOrders.values())
        amount_buy_in_tf  = sum(x[0] for x in buyOrders.values())
        amount_sell_in_tf = sum(x[0] for x in sellOrders.values())
        
        total_data["order_buy"]   += order_buy_in_tf  
        total_data["order_sell"]  += order_sell_in_tf
        total_data["total_buy"]   += amount_buy_in_tf
        total_data["total_sell"]  += amount_sell_in_tf
        total_data["frame_count"] += 1
        
        
        
        print("In TimeFrame. Orders BUY/SELL: {0:05d} / {1:05d}  BTC BUY/SELL: {2:.2f} / {3:.2f}".
              format(order_buy_in_tf, order_sell_in_tf, amount_buy_in_tf, amount_sell_in_tf))
        print("Summary.      Orders BUY/SELL: {0:05d} / {1:05d}  BTC BUY/SELL: {2:.2f} / {3:.2f}".
              format( total_data["order_buy"], total_data["order_sell"], total_data["total_buy"], total_data["total_sell"]))
        print("First price is: {0:.2f} All time price change, % = {1:.2%}".format(total_data["first_price"], cur_price / total_data["first_price"] - 1) )
        print("Total frame left: %s" % (total_data["frame_count"])) 
        buyOrders = {}
        sellOrders = {}
        last_time = cur_time
        last_price = cur_price
    
    
sellOrders = {}
buyOrders  = {}
total_data = {"first_price": 0, 
              "order_buy"  : 0, 
              "order_sell" : 0, 
              "total_buy"  : 0, 
              "total_sell" : 0,
              "frame_count": 0}
last_time = int(round(time.time() * 1000)) 
time_frame_sec = 60
last_price = 0
trade_pair = 'BTCUSDT'


client = Client("api_key", "api_secret")
bm = BinanceSocketManager(client)
# start any sockets here, i.e a trade socket
conn_key = bm.start_trade_socket(trade_pair, callback)
# then start the socket manager
bm.start()
