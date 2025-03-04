import enum

class ProxyState(enum.Enum):
    INIT = 0
    RECEIVE = 1
    PROCESS = 2
    SEND = 3
    CLOSING = 4
    
