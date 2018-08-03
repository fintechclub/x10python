#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests

class OKexClient:
    def __init__(self, public_key, secret):
        self.url = "https://www.okex.com/v2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)

 
    def getCoinList(self, symbol_code=""):
        return self.session.get("%s/spot/markets/currencies" % (self.url)).json()

    def getSymbol(self, symbol_code=""):
        """Get symbol."""
        return None
    
    def getOrderbook(self, symbol_code):
        """Get orderbook. """
        return None
    
    def getAddress(self, currency_code):
        """Get address for deposit."""
        return None
    
    def getAccountBalance(self):
        """Get main balance."""
        return None
    
    def getTradingBalance(self):
        """Get trading balance."""
        return None
    
    def newOrder(self, client_order_id, symbol_code, side, quantity, price=None):
        return None
    
    def getOrder(self, client_order_id, wait=None):
        return None

    def cancelOrder(self, client_order_id):
        return None
    
    def withdraw(self, currency_code, amount, address, network_fee=None):
        return None

    def getTransaction(self, transaction_id):
        """Get transaction info."""
        return None
