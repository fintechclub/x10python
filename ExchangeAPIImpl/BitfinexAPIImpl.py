#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests


# Bitfinex API documentation
# https://docs.bitfinex.com/docs
class Client(object):
    def __init__(self, public_key, secret):
        self.url = "https://api.bitfinex.com/v1"
        self.session = requests.session()
        self.session.auth = (public_key, secret)
        

    def get_symbols(self):
        """Get symbols."""
        return self.session.get("%s/symbols" % (self.url)).json()
