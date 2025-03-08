import enum

class ClientState(enum.Enum):
    INIT = 0
    INPUT = 1
    RECEIVE = 2
    PROCESS = 3
    SEND = 4
    CLOSING = 5
    
