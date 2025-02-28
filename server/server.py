import socket

class Server:
    def __init__(self, server_ip, server_port):

        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None

        self.server_init()

    def server_init(self):
        print("Server Initialize...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        
        print("Server Binding...")
        self.server_socket.bind((self.server_ip, self.server_port))
    
    def server_listen(self):
        while True:
            print("Waiting..")
            self.server_receive()

    def server_receive(self):
        data, client_addr = self.server_socket.recvfrom(1024)

        print("Server Receiving...")
        print(f"Received ({client_addr}): {data.decode()}")

        self.server_response(client_addr)

    def server_response(self, client_addr):
        print("Server Resonding...")
        self.server_socket.sendto("received!".encode(), client_addr)


        