import enum

class ClientState(enum.Enum):
    INIT = 0
    INPUT = 1
    RECEIVE = 2
    PROCESS_RECV = 3
    SEND = 4
    PROCESS_SEND = 5
    CLOSING = 6
    
