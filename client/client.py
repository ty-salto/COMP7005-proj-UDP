import socket
from client_states import ClientState

class Client:
    def __init__(self, client_ip, client_port):

        self.client_ip = client_ip
        self.client_port = client_port


    def client_init(self):
        print("Client Initialize...")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        print("Type your message and press Enter. Type 'exit' to quit.")
        return ClientState.PROCESS
    
    def client_message(self):
        message = input("You: ")

        
        if message.lower() == "exit":
            print("Closing connection.")
            return ClientState.CLOSING
        else:
            return  ClientState.SEND ,message

        
    def client_send(self, mesage):
        print("Client Sending...")
        self.client_socket.sendto(mesage.encode(), (self.client_ip, self.client_port))


    def client_receive(self):
        print("Client Receiving...")
        data, client_addr = self.client_socket.recvfrom(1024)
        print(f"Received ({client_addr}): {data.decode()}")
        return client_addr
    
    def client_closing(self):
        print("Closing client socket...")
        self.client_socket.close()
