#! /usr/bin/env python
# -*- coding: utf-8 -*-

import blockcypher
import pprint
import json
import Blogic
import collections
from Utils.MessageSender import MessageSender
from Utils.Enums import MessageType
from Utils.StopWatch import Timer
import datetime

class WalletAddressChecker:
    
    def __init__(self): 
        self.blogic = Blogic.BusinessLogic()
        self.messageSender = MessageSender(MessageType.TELEGRAM)
        self.wallets = dict({
            "3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r": "wallet: Bitfinex-coldwallet",
            "16ftSEQ4ctQFDtVZiUBusQUjRrGhM3JYwe": "wallet: Binance-wallet",
            "16rCmCmbuWDhPjWTrpQGaU3EPdZF7MTdUk": "wallet: Bittrex-coldwallet",
            "3Nxwenay9Z8Lc9JBiywExpnEFiLp6Afp8v": "wallet: Bitstamp-coldwallet",
            "3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64": "wallet: Huobi-wallet",
            "1KAt6STtisWMMVo5XGdos9P7DBNNsFfjx7": "",
            "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF": "",
            "18rnfoQgGo1HqvVQaAN4QnxjYE7Sez9eca": "wallet: 29043297",
            "1HQ3Go3ggs8pFnXuHVHRytPCq5fGG8Hbhx": "",
            "1PnMfRF2enSZnR6JSexxBHuQnxG8Vo5FVK": "",
            "1AhTjUMztCihiTyA4K6E3QEpobjWLwKhkR": "",
            "1DiHDQMPFu4p84rkLn6Majj2LCZZZRQUaa": "",
            "1EBHA1ckUWzNKN7BMfDwGTx6GKEbADUozX": "",
            "1LdRcdxfbSnmCYYNdeYpUnztiYzVfBEQeC": "",
            "1JCe8z4jJVNXSjohjM4i9Hh813dLCNx2Sy": "",
            "1AC4fMwgY8j9onSbXEWeH6Zan8QGMSdmtA": "",
            "12YygZpCEC8VED2oSMQdWCq5xBnHo9ts1Z": "",
            "3Ap6mixhHLmVtH41YHH94Ut4jBfmqRpzgQ": "",
            "3CqBquEFMYY548fNBz8u2MBw3HKprS3Xft": ""})

    
    def CheckWallets(self):
        print('%s  ---- Start WalletAddressChecker.CheckWallets ----' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        timer = Timer()
        timer.start()
        
        recent_data = {}
        dataFromDB = dict(self.blogic.getWalletsTable())
    
        # Получить обновление балансов по проверяемым кошелькам 
        for address, title in self.wallets.items():
            balance = blockcypher.get_total_balance(address) 
            recent_data[address] = (title, blockcypher.from_satoshis(balance, 'btc') )    
            
        isChange = 0
        text = ""
        for key, value in recent_data.items():
            walletTitle = value[0]
            balance = value[1]
            if dataFromDB.get(key) == None:
                isChange = 1    
                continue
            if dataFromDB.get(key) > balance: 
                isChange = 1 
                text = '\n'.join([text, "С адреса {0:s} {1:s} отправлено {2:.8f} BTC ".format(key, walletTitle, balance - dataFromDB[key])] ) 
            elif dataFromDB.get(key) < balance: 
                isChange = 1 
                text = '\n'.join([text,  "Адрес {0:s} {1:s} получил {2:.8f} BTC".format(key, walletTitle, balance - dataFromDB[key])] )

        if  isChange > 0:
            self.blogic.refreshWalletsTable([(k, v[0], v[1]) for k, v in recent_data.items()])
            self.messageSender.sendMessage(text)
        
        print('----End process WalletAddressChecker.CheckWallets. Time is %s ----' % timer.stop())
        