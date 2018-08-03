#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import hashlib
import hmac
import time #for nonce
import requests


# Bitfinex API documentation
# https://docs.bitfinex.com/docs
class BitfinexClient:
    def __init__(self, api_key, api_secret):    
        self.BASE_URL = "https://api.bitfinex.com/"
        self.KEY = api_key
        self.SECRET = api_secret
        self.API_V2 = "v2"
        self.API_V1 = "v1"
        self.session = requests.session()
        
    def _nonce(self):
        return str(int(round(time.time() * 10000)))

    def _headers(self, path, nonce, body):
        secbytes = self.SECRET.encode(encoding='UTF-8')
        signature = "/api/{0:s}{1:s}{2:s}".format(path, nonce, body)
        sigbytes = signature.encode(encoding='UTF-8')
        h = hmac.new(secbytes, sigbytes, hashlib.sha384)
        hexstring = h.hexdigest()
        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.KEY,
            "bfx-signature": hexstring,
            "content-type": "application/json"
        }

    def _reqA(self, path, api_ver = '', params = {}):
        api_ver =  self.API_V2 if api_ver == '' else api_ver
        nonce = self._nonce()
        body = params
        rawBody = json.dumps(body)
        headers = self._headers("{0:s}/{1:s}".format(api_ver, path), nonce, rawBody)
        url = "{0:s}{1:s}/{2:s}".format(self.BASE_URL, api_ver, path)
        response = requests.post(url, headers = headers, data = rawBody, verify = True)
        if response.status_code == 200:
            return response.json()
        else:
            print('error, status_code = ', response.status_code)
            print(response)
            return 'ERROR'
        
    def _reqP(self, path, api_ver = '', params = {}):
        api_ver =  self.API_V2 if api_ver == '' else api_ver   
        url = "{0:s}{1:s}/{2:s}".format(self.BASE_URL, api_ver, path)
        return self.session.get(url).json()
        
    
    def get_symbols(self):
        """Get symbols."""
        return self._reqP("symbols", self.API_V1)

    def get_tickers(self, symbols):
        return self._reqP("tickers?symbols=%s" % (symbols), self.API_V2)

    def get_orders(self):
        return self._reqA("auth/r/orders")
    
    def get_balances(self):
        return self._reqA("auth/r/wallets")
    
    def get_positions(self):
        return self._reqA("auth/r/positions")
        
    def get_avail_balance(self):
        return self._reqA("auth/calc/order/avail")