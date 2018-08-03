#! /usr/bin/env python
# -*- coding: utf-8 -*-
from x10project import BaseExchangeBL, OKexClient  


class OkexLogic(BaseExchangeBL):
    def __init__(self, account_name='', api_key='', api_secret=''):
        super().__init__("okex", account_name, api_key, api_secret)
        self.okexClient = OKexClient(self.api_key, self.api_secret)
   
    def getSymbolsFromExchange(self):
        data = self.okexClient.getCoinList()
        symbols = set([])
        for item in data["data"]:
            if item["symbol"] not in symbols :
                symbols.add( (item["symbol"], self.exchangeName)) 
        return symbols

