from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import file, client, tools
from x10project import CoinGeckoClient
import os
import pprint
import datetime
import locale
from x10project.utils.messagesender import MessageSender
from x10project.utils.enums import *

class PortfolioMonitor:
    def __init__(self):
        self.CREDENTIALS_FILE = 'test-proj-for-habr-article-1ab131d98a6b.json'  # имя файла с закрытым ключом
        self.SPREADSHEET_ID = '1nGFnlQ7EGio0nULtyU_jVXoX1XmwHFbpndZT_6QeGvo'
        self.PORTFOLIO_SHEET_NAME = "New Portfolio"
        package_dir = os.path.abspath(os.path.dirname(__file__))
        locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
        credential_file = os.path.join(package_dir, 'google_service_account.json')
       
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file,      
                                                                            ['https://www.googleapis.com/auth/spreadsheets.readonly',
                                                                                  'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(Http())
        self.service = build('sheets', 'v4', http = httpAuth)
        self.messageSender = MessageSender(MessageType.TELEGRAM)
        

    def getAssetAmount(self):
        amountAssetRange = self.PORTFOLIO_SHEET_NAME + '!O2'
        result = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                 range=amountAssetRange).execute()
        values = result['values']
        return int(values[0][0])
    

    def getAssets(self, amount):
        portfolioAssetRange = '%s!O3:Y%s'%(self.PORTFOLIO_SHEET_NAME, int(amount)+2)
        results = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                 range=portfolioAssetRange).execute()
        return results['values'] 
        

    def CheckPortfolio(self):
        amountAssetsInPortfolio = self.getAssetAmount()
        assets = self.getAssets(amountAssetsInPortfolio)
        
        portfolio = []
        for item in assets:
            portfolio.append([item[0], item[1], float(item[8]), float(item[9]), float(item[10])])
         
        assetIds = ','.join( (item[1] for item in portfolio) ) 
        geckoClient = CoinGeckoClient()
        prices = geckoClient.get_coinsMarket(ids=assetIds)
        
        
        for item in portfolio:
            item.append( *(price["current_price"] for price in prices if price["id"] == item[1]) )
        
        
        
        #Сколько было потрачено на формирование портфеля, BTC
        originPriceBTC = sum(item[2] for item in portfolio)
        #Сколько было потрачено на формирование портфеля, USD
        originPriceUSD = sum(item[3] for item in portfolio)
        
        #Стоимость портфеля сегодня, BTC
        currentPriceBTC = sum(item[4]*item[5] for item in portfolio)
        currentPriceUSD = currentPriceBTC * float(geckoClient.get_exchangeRates()["rates"]["usd"]["value"])
        
        profitBTC = (currentPriceBTC / originPriceBTC - 1)*100
        profitUSD = (currentPriceUSD / originPriceUSD - 1)*100
        
        
        datetime.datetime.today().strftime("%d-%m-%Y")
        
        message = "Портфель на сегодня {:s} : \n Начальная стоимость(BTC, USD): {:.4f}, {:s}, \n Текущая стоимость(BTC, USD): {:.4f}, {:s}\n Доходность, BTC: {:.2f} ({:.2f}%) \n Доходность, USD: {:s} ({:.2f}%)".format( datetime.datetime.today().strftime("%d-%m-%Y"), 
                                                                                                originPriceBTC,
                                                                                                locale.currency(originPriceUSD, grouping=True),
                                                                                                currentPriceBTC,
                                                                                                locale.currency(currentPriceUSD, grouping=True),
                                                                                                currentPriceBTC - originPriceBTC,
                                                                                                profitBTC,
                                                                                                locale.currency(currentPriceUSD - originPriceUSD, grouping=True),
                                                                                                profitUSD)
        
        #Стоимость портфеля сегодня, USD
        self.messageSender.sendMessage(message)
