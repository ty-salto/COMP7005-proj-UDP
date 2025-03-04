import socket

class Client:
    FIRST_INDEX, SECOND_INDEX = (0,1)

    def __init__(self, client_ip, client_port):

        self.client_ip = client_ip
        self.client_port = client_port


    def client_init(self):
        print("Client Initialize...")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        print("Type your message and press Enter. Type 'exit' to quit.")
        return self.FIRST_INDEX
    
    def client_message(self):
        message = input("You: ")

        
        if message.lower() == "exit":
            print("Closing connection.")
            return self.SECOND_INDEX
        else:
            return  self.FIRST_INDEX ,message

        
    def client_send(self, mesage):
        print("Client Sending...")
        self.client_socket.sendto(mesage.encode(), (self.client_ip, self.client_port))
        return self.FIRST_INDEX


    def client_receive(self):
        print("Client Receiving...")
        data, client_addr = self.client_socket.recvfrom(1024)
        print(f"Received ({client_addr}): {data.decode()}")
        return self.FIRST_INDEX, client_addr
    
    def client_closing(self):
        print("Closing client socket...")
        self.client_socket.close()
