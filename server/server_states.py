import enum

class ServerState(enum.Enum):
    INIT = 0
    LISTEN = 1
    RECEIVE = 2
    PROCESS = 3
    SEND = 4
    CLOSING = 5
    
