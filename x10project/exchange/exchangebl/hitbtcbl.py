#! /usr/bin/env python
# -*- coding: utf-8 -*-

from x10project import BaseExchangeBL, HitBTCClient

class HitBTCLogic(BaseExchangeBL):

    def __init__(self, account_name='', api_key='', api_secret=''):
        super().__init__("hitbtc", account_name, api_key, api_secret)
        self.hitbtcClient = HitBTCClient(api_key, api_secret)
        
      
    def getSymbolsFromExchange(self):      
        data = self.hitbtcClient.get_symbol()
        symbols = set([])
        for item in data:
            if item['baseCurrency'] not in symbols:
                symbols.add( (item['baseCurrency'], self.exchangeName )) 
        return symbols
    