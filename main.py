#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ExchangeAssetMonitor import AssetMonitor
from ExchangeClients.BitfinexClient import BitfinexLogic
import pprint

#bitfinex = BitfinexLogic()
#pprint.pprint( bitfinex.getTickers() )

assetMonitor = AssetMonitor()
assetMonitor.CheckAsset()