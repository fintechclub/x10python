#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ExchangeAssetMonitor import AssetMonitor
from WalletAddressMonitor import WalletAddressChecker

import pprint


def main():
    # print command line arguments
    assetMonitor = AssetMonitor()
    walletChecker = WalletAddressChecker()
    
    for arg in sys.argv[1:]:
        print(arg)
        if arg == "checkAssets":
            assetMonitor.CheckAsset()
        elif arg == "checkWallets":
            walletChecker.CheckWallets()
        elif arg == "checkAll":
            assetMonitor.CheckAsset()
            walletChecker.CheckWallets()
        else: print("Unknown argument: " + arg)
               

if __name__ == "__main__":
    main()
    


