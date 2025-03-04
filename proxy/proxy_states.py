import enum


class ProxyState(enum.Enum):
    INIT = 0
    LISTEN = 1
    RECEIVE = 2
    SEND = 3
    CLOSING = 4
    
