#! /usr/bin/env python
# -*- coding: utf-8 -*-
from kucoin.client import Client 
from ExchangeClients.ExchangeClientBase import BaseExchangeClient

class KucoinChecker(BaseExchangeClient):

    def __init__(self, api_key="1", api_secret="2"):
        super().__init__("kucoin", api_key, api_secret)
              

    def getSymbolsFromExchange(self):
        apiClient = Client(self.api_key, self.api_secret)    
        data = apiClient.get_coin_list()
        symbols = set([])
        for item in data:
            if item['coin'] not in symbols:
                symbols.add( (item['coin'], self.exchangeName ) )
        return symbols
    