#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ExchangeClients.ExchangeClientBase import BaseExchangeClient
from ExchangeAPIImpl.BitfinexAPIImpl import Client
import pprint

# Bitfinex API documenntation  
# https://docs.bitfinex.com/docs/introduction
class BitfinexChecker(BaseExchangeClient):

    def __init__(self, api_key="1", api_secret="2"):
        super().__init__("bitfinex", api_key, api_secret)
        self.bitfinexClient = Client(self.api_key, self.api_secret)
              

    def getSymbolsFromExchange(self):
        data = self.bitfinexClient.get_symbols()
        symbols = set([])
        for item in data:
            if item not in symbols:
                symbols.add( (item, self.exchangeName ) )
        return symbols
    
    def getTicker(self):
        return
        
        