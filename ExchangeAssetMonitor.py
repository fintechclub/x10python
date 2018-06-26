#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
from Utils.MessageSender import *
from ExchangeClients.BinanceClient import BinanceChecker
from ExchangeClients.KucoinClient import KucoinChecker
from ExchangeClients.BitfinexClient import BitfinexChecker
from ExchangeClients.HitBTCClient import HitBTCChecker
from ExchangeClients.IdexClient import IdexChecker
import pprint
import datetime


class AssetMonitor:
    def __init__(self):     
        self.binanceChecker = BinanceChecker()
        self.kucoinChecker = KucoinChecker()
        self.bitfinexChecker = BitfinexChecker()
        self.hitBTCChecker = HitBTCChecker()
        self.idexChecker = IdexChecker()
        
    def CheckAsset(self):
        
        print('----Start process asset on exchanges----')
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        try:
            self.binanceChecker.checkListedAssets()
        except Exception as e:
            print("binanceChecker.checkListedAssets error request. Exception " + str(e))    

        try:
            self.kucoinChecker.checkListedAssets()
        except Exception:
            print("kucoinChecker.checkListedAssets error request")    

        try:
            self.bitfinexChecker.checkListedAssets();
        except Exception:
            print("bitfinexChecker.checkListedAssets error request")    

        try:
            self.hitBTCChecker.checkListedAssets()
        except Exception:
            print("hitBTCChecker.checkListedAssets error request")    

        try:
            self.idexChecker.checkListedAssets()
        except Exception:
            print("idexChecker.checkListedAssets error request")    

        print('----End process----')
        