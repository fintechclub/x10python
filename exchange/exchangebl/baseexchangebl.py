
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from x10project import DataBaseAccess
from x10project.utils.messagesender import MessageSender
from x10project.utils.enums import *

class BaseExchangeBL:
    
    def __init__(self, exchangeName, account_name='', api_key='', api_secret=''):
        self.exchangeName = exchangeName
        self.account_name = account_name
        self.dba = DataBaseAccess()
        self.api_key = api_key
        self.api_secret = api_secret
        self.messageSender = MessageSender(MessageType.CONSOLE)

    def getExchangeName(self):
        return self.exchangeName
    
    def getName(self):
        return self.account_name
  
    def checkListedAssets(self):
        symbolsFromAPI =  self.getSymbolsFromExchange()
        currentExchangeSymbols =  self.dba.getAssetsFromDB(self.exchangeName)
        
        newListedAssets = set(symbolsFromAPI).difference(currentExchangeSymbols)
        convert_first_to_generator = (item[0] for item in newListedAssets)
        newListedAssetsStr = ", ".join(convert_first_to_generator)

        delistedAssets = set(currentExchangeSymbols).difference(symbolsFromAPI)
        convert_first_to_generator = (item[0] for item in delistedAssets)
        newDelistedAssetsStr = ", ".join(convert_first_to_generator)
        
        if len(newListedAssetsStr) > 0: self.messageSender.sendMessage("Нашел новые активы на " + self.exchangeName + ": " + newListedAssetsStr )
        if len(newDelistedAssetsStr) > 0: self.messageSender.sendMessage("Кажется произошел делистинг некоторых активов на " + self.exchangeName+ ": " + newDelistedAssetsStr)
        
        if len(newListedAssetsStr) > 0 or len(newDelistedAssetsStr) > 0:
            self.dba.refreshAssetDB(symbolsFromAPI, self.exchangeName)
        else:
            print ("On " + self.exchangeName + " all the same. Amount of assets is: " + str(len(currentExchangeSymbols)))
            
    def deleteBTC(self):
        self.dba.deleteBTC(self.exchangeName)    
    