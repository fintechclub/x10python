import telegram
from x10project.utils.enums import MessageType
import pprint

class MessageSender:
    def __init__(self, type):
        self.m_type = type
        if self.m_type == MessageType.TELEGRAM:
            self.telegram_bot = telegram.Bot("345714559:AAFattmHvDEHenQLbI5wgTvE0Lhord_aYpQ")
    
    def sendMessage(self, msg):
        if self.m_type == MessageType.TELEGRAM:
            self.sendTelegramMessage(msg)
        if self.m_type == MessageType.CONSOLE:
            self.console(msg)
    
    def sendTelegramMessage(self, msg):  
        #-230337089 - groupId
        #194302348 - user korovaev
        self.telegram_bot.send_message("-230337089", msg)
    
    def console(self, msg):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(msg)
    