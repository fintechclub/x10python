#! /usr/bin/env python
# -*- coding: utf-8 -*-

from binance.client import Client
from ExchangeClients.ExchangeClientBase import BaseExchangeClient

# Binance API documenntation  
# https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
class BinanceChecker(BaseExchangeClient):
    
    def __init__(self, api_key="1", api_secret="2"):
        super().__init__("binance", api_key, api_secret)
        self.binanceClient = Client(self.api_key, self.api_secret)  
        
      
    def getSymbolsFromExchange(self):
        data = self.binanceClient.get_exchange_info()
        symbols = set([])
        for item in data['symbols']:
            if item['baseAsset'] not in symbols:
                symbols.add( (item['baseAsset'], self.exchangeName)) 
        return symbols
        