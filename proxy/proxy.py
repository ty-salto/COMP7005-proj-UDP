import socket
import time
import random


class Proxy:
    def __init__(self, proxy_ip: str, proxy_port: int):
        self.listen_ip= proxy_ip
        self.listen_port = proxy_port
        self.client_ip = None
        self.cient_port = None
        # Edit later
        self.target_ip = "127.0.0.1"
        self.target_port = 8081
        self.client_drop = .1;
        self.server_drop = .1;
        self.client_delay = .9;
        self.server_delay = .9;
        self.server_delay_time = "1-3";
        self.client_delay_time = "1-3";
        self.proxy_socket = socket.socket()

    def proxy_init(self):
        print("Proxy Server Initializing")
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(f"Proxy server listening on {self.listen_ip}:{self.listen_port}")
        self.proxy_socket.bind((self.listen_ip, self.listen_port))

    def proxy_listen(self) -> tuple:
        print("Waiting for Packets")
        return self.proxy_socket.recvfrom(1024)

    def proxy_receive(self, data, addr):
        """
        Receives packet.
        If packet is from the client, client properties updated.
        """
        if not self.is_server(addr[0], addr[1]):
            print("Proxy Receiving from Client")
            self.client_ip, self.client_port = addr[0], addr[1]

        message = data.decode()
        print(f"Recieved{addr}: {message}")
        return addr, message

    def proxy_response(self, address, message):
        ip, port = address
        encoded_message = message.encode()
        if self.is_server(ip, port):
            self.to_client(encoded_message)
        else:
            self.to_server(encoded_message)

    def to_client(self, message):
        print("Proxy forwarding to Client", self.client_ip, self.client_port)
        if self.does_packet_drop(self.server_drop):
            print("Server Packet to Client Fails")
            return
        if self.does_packet_delay(self.server_delay):
            # print(f"Server Packet is delayed by {self.server_delay_time} seconds")
            self.delay_by_seconds(self.server_delay_time);
        self.proxy_socket.sendto(message,(self.client_ip, self.client_port) )

    def to_server(self, message):
        print("Proxy forwarding to Server")
        if self.does_packet_drop(self.client_drop):
            print("Client Packet to Server Fails")
            return
        if self.does_packet_delay(self.client_delay):
            print("Client ", end="")
            self.delay_by_seconds(self.client_delay_time);
        self.proxy_socket.sendto(message,(self.target_ip, self.target_port) )

    def does_packet_delay(self, delay_chance):
        if random.random() < delay_chance:
           return True

    def does_packet_drop(self, delay_chance):
        if random.random() < delay_chance:
            return True

    def delay_by_seconds(self, delay_time):
        """
        Delays packet send by seconds
        """
        lower, upper = delay_time.split("-")
        delay = random.randrange(int(lower), int(upper))
        print(f"Packet is delayed by {delay} second(s)")
        time.sleep(delay)

    def is_server(self, ip, port) -> bool:
        if ip == self.target_ip and port == self.target_port:
            return True
        return False
