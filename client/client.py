import socket

class Client:
    def __init__(self, client_ip, client_port):

        self.client_ip = client_ip
        self.client_port = client_port


    def client_init(self):
        print("Client Initialize...")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        print("Type your message and press Enter. Type 'exit' to quit.")
    
    def client_message(self):
        message = input("You: ")

        return message
        # if message.lower() == "exit":
        #     print("Closing connection.")

        
    def client_send(self, mesage):
        print("Client Sending...")
        self.client_socket.sendto(mesage.encode(), (self.client_ip, self.client_port))


    def client_receive(self):
        print("Client Receiving...")
        data, client_addr = self.client_socket.recvfrom(1024)
        print(f"Received ({client_addr}): {data.decode()}")
        return client_addr
        