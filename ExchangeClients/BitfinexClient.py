#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ExchangeClients.ExchangeClientBase import BaseExchangeClient
from ExchangeAPIImpl.BitfinexAPIImpl import Client
import pprint

# Bitfinex API documenntation  
# https://docs.bitfinex.com/docs/introduction
class BitfinexLogic(BaseExchangeClient):

    def __init__(self, api_key="1", api_secret="2"):
        super().__init__("bitfinex", api_key, api_secret)
        self.bitfinexClient = Client(self.api_key, self.api_secret)
              

    def getSymbolsFromExchange(self):
        data = self.bitfinexClient.get_symbols()
        symbols = set([])
        for item in data:
            if item not in symbols:
                symbols.add( (item.upper(), self.exchangeName ) )
        
        return symbols
    
    def getTickers(self):
        symbols = self.blogic.getAssetsFromDB(self.exchangeName)
        convert_first_to_generator = ("t"+item[0].upper() for item in symbols)
        assetsStr = ",".join(convert_first_to_generator)
        
        tickers = self.bitfinexClient.get_tickers(assetsStr)
        result = set([])
        for item in tickers:
            result.add( ( (item[0])[1:], round(item[7], 6)  ))
        
        return result
        
        