from binance.websockets import BinanceSocketManager
from binance.client import Client as BinanceClient
import json
import pprint
import time
import datetime
import sys
from x10project.utils.messagesender import MessageSender
from x10project.utils.enums import *



def UserEventCallback(msg):
    global messageSender
    if msg['e'] == 'executionReport':
        order_pair = msg['s']
        order_type = msg['o']
        order_side = msg['S']
        order_qty = msg['q']
        order_price = msg['p']
        order_status = msg['X']
        order_id = msg['i']
        
        
        message = "Зарегистрировано новое событие:\n -Статус: {:s} ({:s})\n -Направление: {:s}\n -Торговая пара: {:s}\n -Цена: {:s}\n -Количество: {:s}\n -Тип: {:s}\n -Идентификатор: {:s}".format(convertOrderStatus(order_status), order_status, 
                                            order_side,
                                            order_pair,  
                                            order_price, 
                                            order_qty, 
                                            order_type,
                                            str(order_id))
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
    
    else: return "Статус неизвестен(?)"
    
    
    
messageSender = MessageSender(MessageType.TELEGRAM)
messageSender.setTelegramRecipient(TelegramRecipient.ARBITRAGE_GROUP)
client = BinanceClient("cpVoAC6GOvchaOtNKEBevnKypS2ruQoz5VMoCZHmF2GqoiVkaQiHGO8eFObwXkPn", "xaLFuFrLUL89pnXRTwKcLggT7HgLD3rcKSzWGza6ZHE9twsvD5HsQqwrRGJHGWQO")
bm = BinanceSocketManager(client)
key_user = bm.start_user_socket(UserEventCallback)
# then start the socket manager
bm.start()
