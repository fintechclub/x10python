#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
from x10project import BinanceLogic, KucoinLogic, BitfinexLogic, HitBTCLogic, IdexLogic, OkexLogic
from x10project.utils.messagesender import MessageSender
from x10project.utils.enums import Exchange
import datetime
import pprint


class AssetMonitor:
    def __init__(self):     
        self.exchangeClients={
                              Exchange.BINANCE: BinanceLogic(),
                              Exchange.KUCOIN: KucoinLogic(),
                              Exchange.BITFINEX: BitfinexLogic(),
                              Exchange.HITBTC: HitBTCLogic(),
                              Exchange.IDEX: IdexLogic(),
                              Exchange.OKEX: OkexLogic()
                            }
        
    def CheckAsset(self, exchange=Exchange.ALL):
        print('%s  ----Start AssetMonitor.CheckAsset----' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        if exchange != Exchange.ALL and exchange in self.exchangeClients:
            self.exchangeClients[exchange].checkListedAssets()
        else:
            for key, value in self.exchangeClients.items():
                try:
                    value.checkListedAssets()
                except Exception as e:
                    print("%s.checkListedAssets error request. Exception %s" % (value.__class__.__name__, str(e)))       

        print('----End process AssetMonitor.CheckAsset----')
        