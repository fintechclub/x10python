#! /usr/bin/env python
# -*- coding: utf-8 -*-
import locale
from termcolor import colored, cprint
import pprint
from x10project import BaseExchangeBL, BitfinexClient 

# Bitfinex API documenntation  
# https://docs.bitfinex.com/docs/introduction
class BitfinexLogic(BaseExchangeBL):

    def __init__(self, account_name='', api_key='', api_secret=''):
        super().__init__("bitfinex", account_name, api_key, api_secret)
        self.bitfinexClient = BitfinexClient(self.api_key, self.api_secret)
        locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
              

    def getSymbolsFromExchange(self):
        data = self.bitfinexClient.get_symbols()
        symbols = set([])
        for item in data:
            if item not in symbols:
                symbols.add( (item.upper(), self.exchangeName ) )
        return symbols
    
    def getTickers(self):
        symbols = self.blogic.getAssetsFromDB(self.exchangeName)
        convert_first_to_generator = ("t"+item[0].upper() for item in symbols)
        assetsStr = ",".join(convert_first_to_generator)
        
        tickers = self.bitfinexClient.get_tickers(assetsStr)
        result = set([])
        for item in tickers:
            result.add( ( (item[0])[1:], round(item[7], 6)  ))
        return result
        
    #Проверяет наличие стопоп для окрытых позиций и их достаточность - весь ли объем закрывает стоп-ордер(ы) 
    def checkExistStopOrders(self, positionList, orderList):
        order_pairs = [row[0] for row in orderList]
        msg=''
        for position in positionList:
            if position[0] not in order_pairs:
                msg += "Для пары %s нет стоп ордера \n" % (position[0])
            else:
                index = order_pairs.index(position[0])
                if position[1] + orderList[index][1] != 0:
                    msg += "Для пары %s есть стоп ордер, но количество меньше чем в позиции %s/%s \n" % (position[0], position[1], orderList[index][1])
        return msg

    #Возвращает просадку от баланса при срабатывании стопов (в абсолютном выражении, в процентах) 
    def calculateAccountStopLostRisk(self, balance, orders):
        return 0
    
    
    def getBalance(self):
        api_balances = self.bitfinexClient.get_balances()
        
        #получить маржинальный баланс счета без учета PL по открытым позициям
        return sum(item[2] for item in api_balances if item[0] == 'margin' and item[1] == 'USD')    

    def getPositions(self):
        api_positions = self.bitfinexClient.get_positions()
        
        if api_positions == "ERROR":
            return None;
        
        positions_list = list()
        for item in api_positions:
            pair = item[0]
            amount = item[2]
            base_price = item[3]
            pl = item[6]
            price_liq = item[8]
            positions_list.append( (pair, amount, base_price, pl, price_liq) )
        
        return positions_list

    def getOrders(self):
        api_orders = self.bitfinexClient.get_orders()
        if api_orders == "ERROR":
            return None;
        
        orders_list = list()
        for item in api_orders:
            if item[8] == 'STOP LIMIT' and item[13] == 'ACTIVE':
                #pair, amount, price
                orders_list.append( (item[3], item[6], item[16]) )

        return orders_list
    
    def _positionToString(self, positions, prices):
        
        result=''
        for item in positions:
            result += '🔹 Инструмент: {:s},\n   Количество: {:.2f},\n   Базовая цена: {:s},\n   Текущая цена: {:s},\n   Цена ликвидации: {:s},\n   PL: {:s}\n'.format(item[0], 
                            item[1],
                            locale.currency(item[2], grouping=True),
                            locale.currency(prices[item[0]], grouping=True),
                            locale.currency(item[4], grouping=True),
                            locale.currency(item[3], grouping=True))
        return result
    
    def getTickers(self, symbols):
        tickers_api = self.bitfinexClient.get_tickers(symbols)
        result = dict()
        for item in tickers_api:
            result[item[0]] = item[10]
            
        return result
        
        
    def getCommonAccountInfo(self):
        balance = self.getBalance()
        positions = self.getPositions()
        orders = self.getOrders()
        prices = self.getTickers(','.join(x[0] for x in positions))
        
        checkError = "Не удалось прочитать данные по указанным API ключам" if balance == None or orders == None or positions == None else ''
        
        if checkError != '': 
            return checkError

        '''
        print(colored("\n---Balance---", "green"))
        pprint.pprint(balance)
        
        print(colored("\n---My Orders---", "green"))
        pprint.pprint(orders)    
        
        print(colored("\n---My Positions---", "green"))
        pprint.pprint(positions)    
        '''
        pl = sum(x[3] for x in positions) 
        commonProfit = self.calculateAccountStopLostRisk(balance, orders)
        return "\nОткрыто позиций: {:d}, \nДанные по позициям: \n{:s} \nБаланс аккаунта: {:s}, \nPL: {:s},  \nБаланс(PL): {:s} ({:.2f}%), \nОбщий риск баланса по стопам: {:.2f}% \n".format(len(positions),  
                 self._positionToString(positions, prices),
                 locale.currency(balance, grouping=True), 
                 locale.currency(pl, grouping=True), 
                 locale.currency(balance + pl, grouping=True), 
                 ((balance + pl) / (balance-1 if balance > 0 else pl)) * 100,
                commonProfit)
        