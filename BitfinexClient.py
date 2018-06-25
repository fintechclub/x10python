#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ExchangeClientBase import BaseExchangeClient
import json
import requests



class BitfinexChecker(BaseExchangeClient):

    def __init__(self, api_key="1", api_secret="2"):
        super().__init__("bitfinex", api_key, api_secret)
              

    def getSymbolsFromExchange(self):
        #https://api.bitfinex.com/v2/tickers?symbols=ALL
        response = requests.get("https://api.bitfinex.com/v1/symbols")
        data = response.json()
        
        symbols = set([])
        for item in data:
            if item not in symbols:
                symbols.add( (item, self.exchangeName ) )
        return symbols
        