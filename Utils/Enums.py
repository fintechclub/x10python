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