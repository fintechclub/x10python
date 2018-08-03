from enum import Enum

class MessageType(Enum):
    CONSOLE = 1
    TELEGRAM = 2

class Exchange(Enum):
    BITFINEX = 1
    BINANCE = 2
    HITBTC = 3
    KUCOIN = 4
    IDEX = 5
    OKEX = 6
    ALL = 7
    
class TelegramRecipient(Enum):
    ARBITRAGE_GROUP="-318829342"
    PORTFOLIO_OBSERVER_GROUP="-230337089"
    KOROVAEV_USER="194302348"
         