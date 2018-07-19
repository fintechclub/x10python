#! /usr/bin/env python
# -*- coding: utf-8 -*-
from okex_rest_api import okex_rest_api as OKexClient
from x10project import BaseExchangeBL 


class OkexLogic(BaseExchangeBL):
    def __init__(self, account_name='', api_key='', api_secret=''):
        super().__init__("okex", account_name, api_key, api_secret)
        self.okexClient = OKexClient.KUPINET('freeApi').Stocks('Okex')
   
    def getSymbolsFromExchange(self):
        data = self.okexClient.getAllPairs()
        symbols = set([])
        for item in data["results"]:
            if item["coin_from"] not in symbols :
                symbols.add( (item["coin_from"], self.exchangeName)) 
        return symbols

