#! /usr/bin/env python
# -*- coding: utf-8 -*-

from binance.client import Client as BinanceClient
from x10project import BaseExchangeBL 

# Binance API documenntation  
# https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
class BinanceLogic(BaseExchangeBL):
    
    def __init__(self, account_name='', api_key='', api_secret=''):
        super().__init__("binance", account_name, api_key, api_secret)
        self.binanceClient = BinanceClient(self.api_key, self.api_secret)  
        
      
    def getSymbolsFromExchange(self):
        data = self.binanceClient.get_exchange_info()
        symbols = set([])
        for item in data['symbols']:
            if item['baseAsset'] not in symbols:
                symbols.add( (item['baseAsset'], self.exchangeName)) 
        return symbols
        