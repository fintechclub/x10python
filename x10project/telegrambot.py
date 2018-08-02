
import logging
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram import (ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)
from x10project import AccountCreator


class BotHelper:
    def __init__(self):
        self.accCreator = AccountCreator()
        self.availAcc = self.accCreator.getAvailiableAccounts() 
        self.updater = Updater(token='345714559:AAFattmHvDEHenQLbI5wgTvE0Lhord_aYpQ')
        dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


        self.MAIN_MENU, self.PORTFOLIO_ITEM, self.SHOW_ACC_INFO = range(3)
           
        main_menu_keyboard = [['☠️ Account', 'Command2'],
                            ['Command3','Command4']]
        
        #Маркап для основного меню
        self.main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=True)
        #Маркап для меню в пункте Account
        keyboard = [[InlineKeyboardButton("Андрей", callback_data='andrey'),
                 InlineKeyboardButton("Рустам", callback_data='rustam')],

                [InlineKeyboardButton("Игорь", callback_data='igor'), 
                InlineKeyboardButton("Арсений", callback_data='arsen'),
                InlineKeyboardButton("Покров", callback_data='pokrov'),
                ]]
        self.account_reply_markup = InlineKeyboardMarkup(keyboard)
        
        
        conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', self._startCommand)],

        states = { 
            self.MAIN_MENU: [RegexHandler('^(.*Account)$',
                                    self._accountItemChoose,
                                    pass_user_data=True)
                       ]
        },

        fallbacks=[RegexHandler('^Done$', self.done, pass_user_data=True)]
        )

        dispatcher.add_handler(conv_handler)
        dispatcher.add_handler(CallbackQueryHandler(self._button))    
    
    

    #обработчик команды /start
    def _startCommand(self, bot, update):
        user = update.message.from_user
        
        '''
        send_message(chat_id=update.message.chat_id, 
                         text="Приветствую тебя %s!  Что интересует? Я знаю команды:\n 1. /acc 'код аккаунта'\n\n Вот какие аккаунты мне известны: %s" % (user["first_name"], ', '.join(self.availAcc)))
        '''
        
        update.message.reply_text(
        "Приветствую тебя, %s!  Выбирай что пожелаешь..." % (user["first_name"]),
        reply_markup = self.main_menu_markup)
        
        return self.MAIN_MENU
    
    
    def _accountItemChoose(self, bot, update, user_data):
        update.message.reply_text('Выбери аккаунт:', reply_markup=self.account_reply_markup)
        return self.MAIN_MENU
    
    #обработчик    
    def _button(self, bot, update):    
        query = update.callback_query
        acc_code = update.message.text
        print(acc_code)
        
        msg = '' if acc_code in self.availAcc else "Для выполнения команды мне нужен аргумент. Одно из следующих значений: " + ', '.join(self.availAcc)

        if msg == '':
            msg = self.accCreator.getAccount(acc_code).getCommonAccountInfo() if acc_code in self.availAcc else "Такого аккаунта я не знаю("

        update.message.reply_text(msg, reply_markup = self.account_menu_markup)    
        
    
        
    def done(self, bot, update, user_data):
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_text("I learned these facts about you:"
                                  "{}"
                                  "Until next time!".format('facts_to_str(user_data)'))

        user_data.clear()
        return ConversationHandler.END
 
        
    #обработчик команды /caps    
    def _helpCommand(self, bot, update):
        text_commands = '1. /acc [{:s}] - Выводит информацию по заданному аккаунту \n'.format(', '.join(self.availAcc))
        bot.send_message(chat_id=update.message.chat_id, text=text_commands)

    
    #Обработчик неизвестной команды
    def _unknownCommand(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Я не знаю этой команды😔")
    
    
    def done(bot, update, user_data):
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_text("I learned these facts about you:"
                                  "{}"
                                  "Until next time!".format("facts_to_str(user_data)"))

        user_data.clear()
        return ConversationHandler.END
    
    #Запуск слушателя команд бота    
    def start(self): 
        self.updater.start_polling()
        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()