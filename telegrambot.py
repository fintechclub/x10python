
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from x10project import AccountCreator


class BotHelper:
    def __init__(self):
        self.accCreator = AccountCreator()
        self.availAcc = self.accCreator.getAvailiableAccounts()

        self.updater = Updater(token='345714559:AAFattmHvDEHenQLbI5wgTvE0Lhord_aYpQ')
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


        echo_handler = MessageHandler(Filters.text, self._echoCommand)
        start_handler = CommandHandler('start', self._startCommand)
        caps_handler = CommandHandler('caps', self._capsCommand, pass_args=True)
        account_handler = CommandHandler('acc', self._accCommand, pass_args=True)
        unknown_handler = MessageHandler(Filters.command, self._unknownCommand)


        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(echo_handler)
        self.dispatcher.add_handler(caps_handler)
        self.dispatcher.add_handler(account_handler)
        self.dispatcher.add_handler(unknown_handler)

    def _startCommand(self, bot, update):
        user = update.message.from_user
        bot.send_message(chat_id=update.message.chat_id, 
                         text="Приветствую тебя %s!  Что интересует? Я знаю команды:\n 1. /acc 'код аккаунта'\n\n Вот какие аккаунты мне известны: %s" % (user["first_name"], ', '.join(self.availAcc)))

    def _echoCommand(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def _capsCommand(self, bot, update, args):
        text_caps = ' '.join(args).upper()
        bot.send_message(chat_id=update.message.chat_id, text=text_caps)

    def _accCommand(self, bot, update, args):
        msg = '' if len(args) == 1 and args[0] in self.availAcc else "Для выполнения команды мне нужен аргумент. Одно из следующих значений: " + ', '.join(self.availAcc)

        if msg == '':
            acc_code = args[0]
            msg = self.accCreator.getAccount(acc_code).getCommonAccountInfo() if acc_code in self.availAcc else "Я тебя не понимаю, Брат!"

        bot.send_message(chat_id=update.message.chat_id, text=msg)

    def _unknownCommand(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Извини, Брат. Я не знаю этой команды😔")
    
    def test(self, acc_code):
        print(self.accCreator.getAccount(acc_code).getCommonAccountInfo())
        
    def start(self): 
        self.updater.start_polling()