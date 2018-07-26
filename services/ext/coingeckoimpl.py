#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests

class CoinGeckoClient:
    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3"
        self.session = requests.session()

    def get_coinsList(self):
        """List all supported coins id, name and symbol (no pagination required)"""
        return self.session.get("%s/coins/list" % (self.url)).json()
    
    def get_coins(self, symbol_id=""):
        """List all coins with data (name, price, market, developer, community, etc)"""
        return self.session.get("%s/coins/%s" % (self.url, symbol_id)).json()

    def get_coinHistory(self, symbol_id="", date=""):
        """Get historical data (name, price, market, stats) at a given date for a coin
        The date of data snapshot in dd-mm-yyyy eg. 30-12-2017"""
        return self.session.get("%s/coins/%s/history?date=%s" % (self.url, symbol_id, date)).json()

    
    def get_coinsMarket(self, vs_currency="btc", ids=""):
        """List all supported coins price, market cap, volume, and market related data (no pagination required) """
        return self.session.get("%s/coins/markets?vs_currency=%s&ids=%s" % (self.url, vs_currency, ids)).json()

    def get_exchangeRates(self):
        """Get BTC-to-Currency exchange rates"""
        return self.session.get("%s/exchange_rates" % (self.url)).json()

    

'''
    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={
                'currency': currency_code, 
                'amount': amount,
                'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
            }).json()
'''
    