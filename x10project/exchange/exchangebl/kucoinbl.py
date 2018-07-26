#! /usr/bin/env python
# -*- coding: utf-8 -*-

from kucoin.client import Client as KucoinClient
from x10project import BaseExchangeBL 

class KucoinLogic(BaseExchangeBL):

    def __init__(self, account_name='', api_key='', api_secret=''):
        super().__init__("kucoin", account_name, api_key, api_secret)
        self.kucoinClient = KucoinClient(self.api_key, self.api_secret)
              

    def getSymbolsFromExchange(self):  
        data = self.kucoinClient.get_coin_list()
        symbols = set([])
        for item in data:
            if item['coin'] not in symbols:
                symbols.add( (item['coin'], self.exchangeName ) )
        return symbols
    