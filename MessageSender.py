import telegram
import pprint

telegram_bot = telegram.Bot("345714559:AAFattmHvDEHenQLbI5wgTvE0Lhord_aYpQ")
    
def sendMessage(msg):
    sendTelegramMessage(msg)
    #console(msg)
    
def sendTelegramMessage(msg):  
    #-230337089 - groupId
    #194302348 - user korovaev
    telegram_bot.send_message("-230337089", msg)
    
def console(msg):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(msg)
    