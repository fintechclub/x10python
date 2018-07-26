
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from idex.client import Client as IdexClient
from x10project import BaseExchangeBL 


class IdexLogic(BaseExchangeBL):

    def __init__(self, account_name='', api_key="0x0000000000000000000000000000000000000000", api_secret="0xvxdlk4xjau61mzedukz40us75qqxm9uahimpn912rmm36ai1d45sn7wx4qg6uhaw"):
        super().__init__("idex", account_name, api_key, api_secret)
        self.idexClient = IdexClient(self.api_key, self.api_secret)   
        
      
    def getSymbolsFromExchange(self):
        data = self.idexClient.get_currencies()
        symbols = set([])
        for item in data:
            if item not in symbols and item != '000':
                symbols.add( (item, self.exchangeName)) 
        return symbols
