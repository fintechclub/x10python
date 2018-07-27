import telegram
from x10project.utils.enums import MessageType, TelegramRecipient
import pprint

class MessageSender:
    def __init__(self, type):
        self.m_type = type
        if self.m_type == MessageType.TELEGRAM:
            #reqProxy = telegram.utils.request.Request(proxy_url="socks5://139.59.191.125:1080", urllib3_proxy_kwargs={'username': 'x10telega', 'password': '31415'})
            
            self.telegram_bot = telegram.Bot("345714559:AAFattmHvDEHenQLbI5wgTvE0Lhord_aYpQ")
            self.telegramRecipient = TelegramRecipient.PORTFOLIO_OBSERVER_GROUP
    
    def setTelegramRecipient(self, recipient=TelegramRecipient.PORTFOLIO_OBSERVER_GROUP):
        self.telegramRecipient = recipient
        
    def sendMessage(self, msg):
        if self.m_type == MessageType.TELEGRAM:
            self._sendTelegramMessage(msg)
        if self.m_type == MessageType.CONSOLE:
            self._console(msg)
    
    def _sendTelegramMessage(self, msg):  
        self.telegram_bot.send_message(self.telegramRecipient.value, msg)
    
    def _console(self, msg):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(msg)
    