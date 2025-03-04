import socket
import time
import random
from utils.helper import valid_fixed_or_range_number
import threading
import proxy.display_options as display


class Proxy:
    """
    Proxy class for UDP proxy server
    """
    HUNDRED = 100
    def __init__(self, proxy_ip: str, proxy_port: int):
        self.listen_ip= proxy_ip
        self.listen_port = proxy_port
        self.client_ip = None
        self.cient_port = None
        # Edit later
        self.target_ip = "127.0.0.1"
        self.target_port = 8081
        self.client_drop = 10 / self.HUNDRED
        self.server_drop = 10 / self.HUNDRED
        self.client_delay = 90 / self.HUNDRED
        self.server_delay = 90 / self.HUNDRED
        self.server_delay_time = "1-3"
        self.client_delay_time = "2"
        self.proxy_socket = socket.socket()
        self.running = True
        self.start_monitoring()

    def proxy_init(self):
        """
        Initializes proxy server

        @return: None
        """
        print("Proxy Server Initializing")
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(f"Proxy Ready - server is listening on {self.listen_ip}:{self.listen_port}")
        self.proxy_socket.bind((self.listen_ip, self.listen_port))
        display.options()



    def proxy_listen(self) -> tuple:
        """
        Listens for packets from client/server

        @return: data and address of client/server
        """
        print("Waiting for Packets")
        return self.proxy_socket.recvfrom(1024)

    def proxy_receive(self, data: bytes, addr: tuple) -> tuple:
        """
        Receives packet from client/server

        If packet is from the client, client properties updated.

        @param data: data received from client/server
        @param addr: address of client/server
        """
        if not self.is_server(addr[0], addr[1]):
            print("Proxy Receiving from Client")
            self.client_ip, self.client_port = addr[0], addr[1]

        message = data.decode()
        print(f"Recieved{addr}: {message}")
        return addr, message

    def proxy_response(self, address: tuple, message: str):
        """
        Sends response to client/server

        @param address: address of client/server
        @param message: message to send to client/server
        """
        ip, port = address
        encoded_message = message.encode()
        if self.is_server(ip, port):
            self.to_client(encoded_message)
        else:
            self.to_server(encoded_message)

    def to_client(self, message: bytes):
        """
        Sends message to client

        @param message: message to send to client
        """
        print("Proxy forwarding to Client", self.client_ip, self.client_port)
        if self.does_packet_drop(self.server_drop):
            print("Server Packet to Client Fails")
            return
        if self.does_packet_delay(self.server_delay):
            # print(f"Server Packet is delayed by {self.server_delay_time} seconds")
            self.delay_by_seconds(self.server_delay_time);
        self.proxy_socket.sendto(message,(self.client_ip, self.client_port) )

    def to_server(self, message: bytes):
        """
        Sends message to server

        @param message: message to send to server
        """
        print("Proxy forwarding to Server")
        if self.does_packet_drop(self.client_drop):
            print("Client Packet to Server Fails")
            return
        if self.does_packet_delay(self.client_delay):
            print("Client ", end="")
            self.delay_by_seconds(self.client_delay_time);
        self.proxy_socket.sendto(message,(self.target_ip, self.target_port) )

    def does_packet_delay(self, delay_chance: float):
        """
        Determines if packet should be delayed

        @param delay_chance: probability of packet being delayed
        @return: True if packet should be delayed, False otherwise
        """
        if random.random() < delay_chance:
           return True

    def does_packet_drop(self, delay_chance):
        """
        Determines if packet should be dropped

        @param delay_chance: probability of packet being dropped
        @return: True if packet should be dropped, False otherwise
        """
        if random.random() < delay_chance:
            return True

    def delay_by_seconds(self, delay_time):
        """
        Delays packet send by seconds

        @param delay_time: range of delay time in seconds
        """
        if "-" in delay_time:
            lower, upper = delay_time.split("-")
            delay = random.randrange(int(lower), int(upper)) if valid_fixed_or_range_number(lower) and valid_fixed_or_range_number(upper) else 0
            print(f"Packet is delayed by {delay} second(s)")
            time.sleep(delay)
        else:
            delay = int(delay_time)
            print(f"Packet is delayed by {delay} second(s)")
            time.sleep(delay)

    def is_server(self, ip, port) -> bool:
        if ip == self.target_ip and port == self.target_port:
            return True
        return False

    def monitor_user_input(self):
            """
            Monitors user input to change proxy parameters dynamically.
            """
            while self.running:
                try:
                    user_input = input("CMD (e.g., 'client_drop 0.2', 1, 2, or q): ").strip().split()
                    if len(user_input) == 1:
                        command = user_input[0]
                        if command == "1":
                            print("Usage to change proxy parameters: <parameter> <value>")
                            display.available_params()
                        elif command == "2":
                            display.current_setup(
                                self.client_drop,
                                self.server_drop,
                                self.client_delay,
                                self.server_delay,
                                self.client_delay_time,
                                self.server_delay_time
                            )
                        elif command == "3" or command == "q":
                            self.proxy_socket.close()
                            exit()
                    elif len(user_input) == 2:
                        param, value = user_input
                        self.update_parameter(param, value)
                    else:
                        print("Invalid command. Please enter a valid command.")
                except ValueError:
                    print("Invalid value. Please enter a valid number.")
                except Exception as e:
                    print(f"Error: {e}")

    def update_parameter(self, param, value):
        """
        Update a parameter value.

        @param param: The parameter to update.
        @param value: The new value for the parameter.
        @precondition: param must be a valid parameter name.
        @precondition: values must be between 0 and 100.
        """
        valid_params = {
            "client_drop": float,
            "server_drop": float,
            "client_delay": float,
            "server_delay": float,
            "client_delay_time": str,
            "server_delay_time": str,
        }

        if param in valid_params:
            if param == "client_delay_time" or param == "server_delay_time":
                setattr(self, param, valid_params[param](value))
            else:
                setattr(self, param, valid_params[param](value)/self.HUNDRED)
            print(f"Updated {param} to {getattr(self, param)}")
        else:
            print(f"Invalid parameter: {param}")
            print("Invalid input. Usage: <parameter> <value>\n")


    def start_monitoring(self):
        """
        Starts the user input monitoring thread.
        """
        self.running = True
        threading.Thread(target=self.monitor_user_input, daemon=True).start()
