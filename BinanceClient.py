#! /usr/bin/env python
# -*- coding: utf-8 -*-
from binance.client import Client
from ExchangeClientBase import BaseExchangeClient

class BinanceChecker(BaseExchangeClient):

    def __init__(self, api_key="1", api_secret="2"):
        super().__init__("binance", api_key, api_secret)
        
      
    def getSymbolsFromExchange(self):
        binanceClient = Client(self.api_key, self.api_secret)    
        data = binanceClient.get_exchange_info()
        symbols = set([])
        for item in data['symbols']:
            if item['baseAsset'] not in symbols:
                symbols.add( (item['baseAsset'], self.exchangeName)) 
        return symbols
