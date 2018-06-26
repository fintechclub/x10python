#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ExchangeAPIImpl.HitBTCAPIImpl import Client
from ExchangeClients.ExchangeClientBase import BaseExchangeClient


class HitBTCLogic(BaseExchangeClient):

    def __init__(self, api_key="1", api_secret="2"):
        super().__init__("hitbtc", api_key, api_secret)
        
      
    def getSymbolsFromExchange(self):
        hitbtcClient = Client(self.api_key, self.api_secret)    
        data = hitbtcClient.get_symbol()
        symbols = set([])
        for item in data:
            if item['baseCurrency'] not in symbols:
                symbols.add( (item['baseCurrency'], self.exchangeName )) 
        return symbols
    