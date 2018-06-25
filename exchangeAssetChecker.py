#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
from MessageSender import *
from BinanceClient import BinanceChecker
from KucoinClient import KucoinChecker
from BitfinexClient import BitfinexChecker
from HitBTCClient import HitBTCChecker
from IdexClient import IdexChecker
import pprint
import datetime

binanceChecker = BinanceChecker()
kucoinChecker = KucoinChecker()
bitfinexChecker = BitfinexChecker()
hitBTCChecker = HitBTCChecker()
idexChecker = IdexChecker()

print('----Start process asset on exchanges----')
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

try:
    binanceChecker.deleteBTC()
    binanceChecker.checkListedAssets()
except Exception:
    print("binanceChecker.checkListedAssets error request")    

try:
    kucoinChecker.checkListedAssets()
except Exception:
    print("kucoinChecker.checkListedAssets error request")    

try:
    bitfinexChecker.checkListedAssets();
except Exception:
    print("bitfinexChecker.checkListedAssets error request")    

try:
    hitBTCChecker.checkListedAssets()
except Exception:
    print("hitBTCChecker.checkListedAssets error request")    
    
try:
    idexChecker.checkListedAssets()
except Exception:
    print("idexChecker.checkListedAssets error request")    
    
print('----End process----')