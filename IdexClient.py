from idex.client import Client
from ExchangeClientBase import BaseExchangeClient

class IdexChecker(BaseExchangeClient):

    def __init__(self, api_key="0x0000000000000000000000000000000000000000", api_secret="0xvxdlk4xjau61mzedukz40us75qqxm9uahimpn912rmm36ai1d45sn7wx4qg6uhaw"):
        super().__init__("idex", api_key, api_secret)
        
      
    def getSymbolsFromExchange(self):
        idexClient = Client(self.api_key, self.api_secret)    
        data = idexClient.get_currencies()
        symbols = set([])
        for item in data:
            if item not in symbols and item != '000':
                symbols.add( (item, self.exchangeName)) 
        return symbols
