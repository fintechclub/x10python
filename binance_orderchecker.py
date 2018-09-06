from binance.websockets import BinanceSocketManager
from binance.client import Client as BinanceClient
import json
import pprint
import time
import datetime
import sys
from x10project.utils.messagesender import MessageSender
from x10project.utils.enums import *



def UserExmoEventCallback(msg):
    clientType = "EXMO"
    if msg['e'] == 'executionReport':
        ExecutionReportEventHandler(msg, clientType)
    if msg['e'] == 'outboundAccountInfo':
        OutboundAccountInfoEventHandler(msg, clientType)
    

def UserCEXEventCallback(msg):
    clientType = "CEX.IO"
    if msg['e'] == 'executionReport':
        ExecutionReportEventHandler(msg, clientType) 
    if msg['e'] == 'outboundAccountInfo':
        OutboundAccountInfoEventHandler(msg, clientType)
    
    
def OutboundAccountInfoEventHandler(msg, clientType):
    message = "Баланс аккаунта для работы с биржей {:s}: \n".format(clientType)
    for item in msg['B']:
        free = float(item['f'])
        lock = float(item['l'])
        if free > 0 or lock > 0:
            message += "-{:s} Доступно={:.5f}".format(item['a'], free) if free > 0 else ""
            message += ", В ордере={:.5f}\n".format(lock) if lock > 0 else "\n"
            
    messageSender.sendMessage(message)
    
def ExecutionReportEventHandler(msg, clientType):
    global messageSender
    order_pair = msg['s']
    order_type = msg['o']
    order_side = msg['S']
    order_qty = msg['q']
    order_price = float(msg['p'])
    order_status = msg['X']
    order_id = msg['i']


    if order_status == "FILLED" or order_status == "PARTIALLY_FILLED":
        return

    if order_type == "MARKET" and float(msg['z']) > 0:
        order_price = float(msg['Z']) / float(msg['z'])
        
    if order_type == "MARKET"
        print("Z - {:s} \n".format( msg['Z']))
        print("z - {:s} \n".format(msg['z']))

    message = "Зарегистрировано новое событие:\n -Арбитраж с биржей: {:s}\n -Статус: {:s} ({:s})\n -Тип ордера: {:s}\n -Направление: {:s}\n -Торговая пара: {:s}\n -Цена: {:.5f}\n -Количество: {:s}".format(clientType,
                                        convertOrderStatus(order_status), order_status, 
                                        order_type,
                                        order_side,
                                        order_pair,  
                                        order_price, 
                                        order_qty)
    if order_status == "REJECTED":
        message +=  "\n -Причина отказа: {:s}".format(msg['r'])


    messageSender.sendMessage(message)
    
def convertOrderStatus(statusCode):
    if statusCode == "NEW": return "Создан новый"
    elif statusCode == "CANCELED": return "Отменен"
    elif statusCode == "TRADE": return "Исполнен"
    elif statusCode == "EXPIRED": return "Просрочен"
    elif statusCode == "REJECTED": return "Отклонен"
    elif statusCode == "FILLED": return "Исполнен"
    elif statusCode == "PARTIALLY_FILLED": return "Частично исполнен"
    
    
    else: return "Статус неизвестен(?)"
    
    
    
messageSender = MessageSender(MessageType.TELEGRAM)
messageSender.setTelegramRecipient(TelegramRecipient.ARBITRAGE_GROUP)
#messageSender.setTelegramRecipient(TelegramRecipient.KOROVAEV_USER)

clientArbitrageExmo = BinanceClient("cpVoAC6GOvchaOtNKEBevnKypS2ruQoz5VMoCZHmF2GqoiVkaQiHGO8eFObwXkPn", "xaLFuFrLUL89pnXRTwKcLggT7HgLD3rcKSzWGza6ZHE9twsvD5HsQqwrRGJHGWQO")

clientArbitrageCexIO = BinanceClient("3AXtPzcT9Hrbt0il8DGhlnY8oqSwVDc8XGOOaRYC9PL2mehTGyZz984NvYG561yn", "oyo7KC54D02uCZkfP7Sm7IdW0rHp3LSVhs7sboc8opkkkHTFc4ie0EXP5VN0EpTz")

bmExmo = BinanceSocketManager(clientArbitrageExmo)
key_user = bmExmo.start_user_socket(UserExmoEventCallback)
# then start the socket manager
bmExmo.start()

bmCex = BinanceSocketManager(clientArbitrageCexIO)
key_user2 = bmCex.start_user_socket(UserCEXEventCallback)
# then start the socket manager
bmCex.start()

print("OrderChecker started!")