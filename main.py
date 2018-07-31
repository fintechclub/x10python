#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from x10project import AssetMonitor, WalletAddressMonitor, BotHelper, PortfolioMonitor
import pprint
from x10project import AccountCreator

def main():
    # print command line arguments
  
    assetMonitor = AssetMonitor()
    walletMonitor = WalletAddressMonitor()
    
    for arg in sys.argv[1:]:
        if arg == "checkAssets":
            assetMonitor.CheckAsset()
        elif arg == "checkWallets":
            walletMonitor.CheckWallets()
        elif arg == "checkAll":
            assetMonitor.CheckAsset()
            walletMonitor.CheckWallets()
        elif arg == "startBot":
            bot = BotHelper()
            bot.start()
        elif arg == "test":    
            accCreator = AccountCreator()
            print(accCreator.getAccount("andrey").getCommonAccountInfo())
        elif arg == "portfolio":
            portfolio = PortfolioMonitor()
            portfolio.CheckPortfolio()
        else: print("Unknown argument: " + arg)
    
if __name__ == "__main__":
    main()
    


