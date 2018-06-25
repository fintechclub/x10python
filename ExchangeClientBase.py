import sqlite3
from Blogic import BusinessLogic
import MessageSender

class BaseExchangeClient:
    
    def __init__(self, exchangeName, api_key, api_secret):
        self.exchangeName = exchangeName
        self.blogic = BusinessLogic()
        self.api_key = api_key
        self.api_secret = api_secret

    def getExchangeName(self):
        return self.exchangeName
    
  
    def checkListedAssets(self):
        symbolsFromAPI =  self.getSymbolsFromExchange()
        currentExchangeSymbols =  self.blogic.getAssetsFromDB(self.exchangeName)

        newListedAssets = set(symbolsFromAPI).difference(currentExchangeSymbols)
        convert_first_to_generator = (item[0] for item in newListedAssets)
        newListedAssetsStr = ", ".join(convert_first_to_generator)

        delistedAssets = set(currentExchangeSymbols).difference(symbolsFromAPI)
        convert_first_to_generator = (item[0] for item in delistedAssets)
        newDelistedAssetsStr = ", ".join(convert_first_to_generator)
        
        if len(newListedAssetsStr) > 0: MessageSender.sendMessage("Нашел новые активы на " + self.exchangeName + ": " + newListedAssetsStr )
        if len(newDelistedAssetsStr) > 0: MessageSender.sendMessage("Кажется произошел делистинг некоторых активов на " + self.exchangeName+ ": " + newDelistedAssetsStr)
        
        if len(newListedAssetsStr) > 0 or len(newDelistedAssetsStr) > 0:
            self.blogic.refreshAssetDB(symbolsFromAPI, self.exchangeName)
        else:
            print ("On " + self.exchangeName + " all the same. Amount of assets is: " + str(len(currentExchangeSymbols)))
            
    def deleteBTC(self):
        self.blogic.deleteBTC(self.exchangeName)    
    