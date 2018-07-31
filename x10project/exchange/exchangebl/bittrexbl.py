from x10project import BaseExchangeBL 
from bittrex.bittrex import *
import pprint

#https://github.com/ericsomdahl/python-bittrex
class BittrexLogic(BaseExchangeBL):

    def __init__(self, account_name=None, api_key=None, api_secret=''):
        super().__init__("bittrex", account_name, api_key, api_secret)
        self.bittrexClient = Bittrex(self.api_key, self.api_secret, api_version=API_V1_1) 
    
    
    
    def getTicker(self, symbol):
        self.bittrexClient.get_ticker()
        
        
    def getMarketSummaries(self):
        result = self.bittrexClient.get_market_summaries()
        return result['result']
    
    
    def getTickers(self, symbols):
        market_symbols = self.getMarketSummaries()
        result = dict()
        for item in market_symbols:
            base_c, rated_c = item['MarketName'].split('-')
        
            if base_c == 'BTC' and self._findInList(symbols, rated_c) == True:
                result[rated_c] = item['Last']
        return result
    
    
    def _findInList(self, arr, elem):
        for item in arr:
            if item == elem:
                return True

        return False
    
    def getOrders(self):
        orders = self.bittrexClient.get_open_orders()
        if orders['success'] == False:
            return None
        return  [(item['Exchange'], item['OrderType'], item['Limit'], item['Quantity']) for item in orders['result']]     
        
    def getBalances(self):
        full_balances = self.bittrexClient.get_balances()
        if full_balances['success'] == False:
            return None
        return [(item['Currency'], item['Balance'], item['Available']) for item in full_balances['result'] if item['Balance'] > 0]    
    
    def _balancesToString(self, balances):
        result=''
        for item in balances:
            result += '🔹 Инструмент: {:s},\n   Количество: {:.2f}\n'.format(item[0], 
                                                                            item[1])
        return result
    
    
    def _ordersToString(self, orders):
        result=''
        
        for item in orders:
            result += '{:s} Инструмент: {:s},\n   Тип ордера: {:s}\n   Количество: {:.2f}\n   Цена: {:.7f}\n'.format( '🔴' if item[1]=='LIMIT_SELL' else '🔵', item[0], 
                                                                            item[1], item[3], item[2])
        
        return result if result != '' else 'Отсутствуют'
        
    
    def getCommonAccountInfo(self):
        balances = self.getBalances()
        orders = self.getOrders()
        tickers = self.getTickers( [item[0] for item in balances] )
        
        est_balance = sum(item[1] * tickers[item[0]] for item in balances if item[0] != 'BTC' and item[0] != 'USDT')
        est_balance += sum(item[1] for item in balances if item[0] == 'BTC')
        
        '''
        print(colored("\n---Balance---", "green"))
        pprint.pprint(balance)
        
        print(colored("\n---My Orders---", "green"))
        pprint.pprint(orders)       
        '''
        
        return "Рассчетный баланс: {:.4f}, \nДанные по балансу: \n{:s} \nОткрытые ордера:\n{:s}".format(est_balance,         
                                                                                                       self._balancesToString(balances),   
                                                                                                       self._ordersToString(orders))
                
        