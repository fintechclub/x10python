#! /usr/bin/env python
# -*- coding: utf-8 -*-


from okex_rest_api import okex_rest_api as Client
from ExchangeClients.ExchangeClientBase import BaseExchangeClient



class OkexLogic(BaseExchangeClient):
    def __init__(self, api_key="1", api_secret="2"):
        super().__init__("okex", api_key, api_secret)
   
    def getSymbolsFromExchange(self):
        data = Client.KUPINET('freeApi').Stocks('Okex').getAllPairs()
        symbols = set([])
        for item in data["results"]:
            if item["coin_from"] not in symbols :
                symbols.add( (item["coin_from"], self.exchangeName)) 
        return symbols

