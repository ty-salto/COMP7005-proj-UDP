import socket
from .server_states import ServerState

class Server:
    def __init__(self, server_ip, server_port):

        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None


    def server_init(self):
        print("Server Initialize...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        
        print("Server Binding...")
        self.server_socket.bind((self.server_ip, self.server_port))

        return ServerState.LISTEN

    
    def server_listen(self):

        print("Waiting..")
        data, client_addr = self.server_socket.recvfrom(1024) 
        return ServerState.RECEIVE, data, client_addr # return tuple [data, client_addr]
        

    def server_receive(self, data, client_addr):

        print("Server Receiving...")
        print(f"Received ({client_addr}): {data.decode()}")
        ip, port = client_addr
        return ServerState.SEND, ip, port

    def server_response(self, ip, port):
        print("Server Resonding...")
        self.server_socket.sendto("received!\n".encode(), (ip,port))
        return ServerState.LISTEN


        