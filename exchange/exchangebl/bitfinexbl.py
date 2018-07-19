#! /usr/bin/env python
# -*- coding: utf-8 -*-
import locale
from termcolor import colored, cprint
import pprint
from x10project import BaseExchangeBL, BitfinexClient 

# Bitfinex API documenntation  
# https://docs.bitfinex.com/docs/introduction
class BitfinexLogic(BaseExchangeBL):

    def __init__(self, acc_name='', account_name='', api_key='', api_secret=''):
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
        
    def checkStopOrders(self, positionList, orderList):
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


    def calculateOrderLost(self, positionList, orderList):
        return -40

    
    def getCommonAccountInfo(self):
        api_balances = self.bitfinexClient.get_balances()
        api_orders = self.bitfinexClient.get_orders()
        api_positions = self.bitfinexClient.get_positions()
        pprint.pprint(api_positions)
        
        checkError = "Не удалось прочитать данные по указанным API ключам" if api_balances == "ERROR" or api_orders == "ERROR" or api_positions == "ERROR" else ''
        
        if checkError != '': 
            return checkError

        #получить маржинальный баланс счета без учета PL по открытым позициям
        balance = sum(item[2] for item in api_balances if item[0] == 'margin' and item[1] == 'USD')    

        orders_list = list()
        for item in api_orders:
            if item[8] == 'STOP LIMIT' and item[13] == 'ACTIVE':
                #pair, amount, price
                orders_list.append( (item[3], item[6], item[16]) )

        print(colored("\n---My Orders---", "green"))
        pprint.pprint(orders_list)    

        positions_list = list()
        for item in api_positions:
            pair = item[0]
            amount = item[2]
            base_price = item[3]
            pl = item[6]
            positions_list.append( (pair, amount, base_price, pl) )

        print(colored("\n---My Positions---", "green"))
        pprint.pprint(positions_list)    

        pl = sum(x[3] for x in positions_list) 
        commonProfit = self.calculateOrderLost(positions_list, orders_list)
        return "\nОткрыто позиций: {:d}, \nБаланс: {:s}, \nPL: {:s},  \nБаланс(PL): {:s} ({:.2f}%), \nОбщий риск по стопам: {:.2f}% \n".format(len(positions_list), 
                 locale.currency(balance, grouping=True), 
                 locale.currency(pl, grouping=True), 
                 locale.currency(balance + pl, grouping=True), 
                 ((balance + pl)/balance-1)*100,
                commonProfit)
        