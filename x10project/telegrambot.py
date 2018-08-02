
import logging
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram import (ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)
from x10project import (AccountCreator, PortfolioMonitor)



class BotHelper:
    def __init__(self):
        self.accCreator = AccountCreator()
        self.availAcc = self.accCreator.getAvailiableAccounts() 
        self.updater = Updater(token='345714559:AAFattmHvDEHenQLbI5wgTvE0Lhord_aYpQ')
        self.portfolioMonitor = PortfolioMonitor()
        dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


        self.MAIN_MENU = 0
           
        main_menu_keyboard = [['☠️ Account', '💸 PortfolioInfo'],
                            ['🔒 Item3','🔒 Item4']]
        
        #Маркап для основного меню
        self.main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=False)
        #Маркап для меню в пункте Account
        keyboard = [[InlineKeyboardButton("Андрей", callback_data='andrey'),
                 InlineKeyboardButton("Рустам", callback_data='rustam')],

                [InlineKeyboardButton("Игорь", callback_data='igor'), 
                InlineKeyboardButton("Арсений", callback_data='arsen'),
                InlineKeyboardButton("Покров", callback_data='pokrov'),
                ]]
        self.account_reply_markup = InlineKeyboardMarkup(keyboard)
        

        #dispatcher.add_handler(CommandHandler('start', self._startCommand))
        dispatcher.add_handler(CommandHandler('start', self._startCommand))
        dispatcher.add_handler(RegexHandler('^(.*Account)$',  self._accountItemChoose))
        dispatcher.add_handler(RegexHandler('^(.*PortfolioInfo)$', self._portfolioInfoItemChoose))
        dispatcher.add_handler(RegexHandler('^(.*Item3|.*Item4)$', self._commandItemChoose))
        dispatcher.add_handler(CallbackQueryHandler(self._button))  
        dispatcher.add_error_handler(self.error)
        dispatcher.add_handler(MessageHandler(Filters.command, self._unknownCommand))
    
    
    
    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        print('Update "%s" caused error "%s"', update, error)


    #обработчик команды /start
    def _startCommand(self, bot, update):
        user = update.message.from_user
          
        update.message.reply_text("Приветствую тебя, %s!  Выбирай что пожелаешь..." % (user["first_name"]),
                                reply_markup = self.main_menu_markup)
        
     
    
    
    def _accountItemChoose(self, bot, update):
        bot.send_message(text='Выбери аккаунт:', chat_id=update.message.chat_id, reply_markup=self.account_reply_markup)
        #update.message.reply_text('Выбери аккаунт:', reply_markup=self.account_reply_markup)
        
        
    def _portfolioInfoItemChoose(self, bot, update):
        bot.send_message(text=self.portfolioMonitor.CheckPortfolio(returnText=True), 
                         chat_id=update.message.chat_id, 
                         reply_markup=self.main_menu_markup)
        
    
    def _commandItemChoose(self, bot, update):
        bot.send_message(text='Я пока не знаю, что тебе ответить...(', chat_id=update.message.chat_id, reply_markup=self.main_menu_markup)
       
    
    #обработчик    
    def _button(self, bot, update):    
        query = update.callback_query
        acc_code = query.data
        
        msg = '' if acc_code in self.availAcc else "Для выполнения команды мне нужен аргумент. Одно из следующих значений: " + ', '.join(self.availAcc)

        try:
            if msg == '':
                msg = self.accCreator.getAccount(acc_code).getCommonAccountInfo() if acc_code in self.availAcc else "Такого аккаунта я не знаю("
        except: 
            msg = "❌ Не могу получить данные для выбранного аккаунта"
        
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                    reply_markup = self.account_reply_markup)

 
        
    #обработчик команды /caps    
    def _helpCommand(self, bot, update):
        text_commands = '1. /acc [{:s}] - Выводит информацию по заданному аккаунту \n'.format(', '.join(self.availAcc))
        bot.send_message(chat_id=update.message.chat_id, text=text_commands)

    
    #Обработчик неизвестной команды
    def _unknownCommand(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Я не знаю этой команды😔")
    
    
    #Запуск слушателя команд бота    
    def start(self): 
        self.updater.start_polling()
        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()