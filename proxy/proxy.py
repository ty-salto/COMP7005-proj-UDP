import socket
import time
import random
from chart.chart import Chart
from chart.socket_chart import SocketChart
from utils.helper import valid_fixed_or_range_number
import threading
import proxy.display_options as display


class Proxy:
    """
    Proxy class for UDP proxy server
    """
    HUNDRED = 100

    def __init__(
            self,
            proxy_ip: str,
            proxy_port: int,
            target_ip: str = "127.0.0.1",
            target_port: int = 8081,
            client_drop: float = 0.5,
            server_drop: float = 0.5,
            client_delay: float = 0.5,
            server_delay: float = 0.5,
            server_delay_time: str = "1-3",
            client_delay_time: str = "1-3"
        ):
            self.listen_ip = proxy_ip
            self.listen_port = proxy_port
            self.client_ip = None
            self.client_port = None
            self.target_ip = target_ip
            self.target_port = target_port
            self.client_drop = client_drop / Proxy.HUNDRED
            self.server_drop = server_drop / Proxy.HUNDRED
            self.client_delay = client_delay / Proxy.HUNDRED
            self.server_delay = server_delay / Proxy.HUNDRED
            self.server_delay_time = server_delay_time
            self.client_delay_time = client_delay_time
            self.proxy_socket = socket.socket()
            self.chart = Chart()
            self.socket_chart = SocketChart("Proxy")
            self.display_options = False
            self.monitor_thread_condition = True
            self.monitor_thread = threading.Thread(target=self.monitor_user_input, daemon=True)
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
        Listens for packets from client/server and if monitor user thread is False to trigger chart

        @return: data and address of client/server
        """
        print("Waiting for Packets")
        print("CMD (e.g., 'client_drop 0.2', 1) options, 2) current_setup, or 3/q quit): ".rstrip())
        while True:
            if not self.monitor_thread_condition:
                self.close()
            try:
                self.proxy_socket.settimeout(1)
                packet = self.proxy_socket.recvfrom(1024)
                ip, port = packet[0], packet[1]
                return ip, port
            except socket.timeout:
                if not self.monitor_thread_condition:
                    self.close()
    def proxy_receive(self, data: bytes, addr: tuple) -> tuple:
        """
        Receives packet from client/server

        If packet is from the client, client properties updated.

        @param data: data received from client/server
        @param addr: address of client/server
        """
        if not self.is_server(addr[0], addr[1]):
            print("Proxy Receiving from Client")
            self.chart.increment_chart_param("client_packet_received")
            self.client_ip, self.client_port = addr[0], addr[1]
        elif self.is_server(addr[0], addr[1]):
            self.chart.increment_chart_param("server_packet_received")

        message = data.decode()
        print(f"Recieved: {addr}: {message}")
        return addr, message

    def proxy_response(self, address: tuple, message: str) -> None:
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

    def to_client(self, message: bytes) -> None:
        """
        Sends message to client

        @param message: message to send to client
        """
        print("Proxy forwarding to Client", self.client_ip, self.client_port)
        if self.does_packet_drop(self.server_drop):
            print("Server Packet to Client Fails")
            self.chart.increment_chart_param("server_packet_dropped")
            return
        if self.does_packet_delay(self.server_delay):
            # print(f"Server Packet is delayed by {self.server_delay_time} seconds")
            self.delay_by_seconds(self.server_delay_time);
        self.chart.increment_chart_param("server_packet_sent")
        self.proxy_socket.sendto(message, (self.client_ip, self.client_port))

    def to_server(self, message: bytes) -> None:
        """
        Sends message to server

        @param message: message to send to server
        """
        print("Proxy forwarding to Server")
        if self.does_packet_drop(self.client_drop):
            print("Client Packet to Server Fails")
            self.chart.increment_chart_param("client_packet_dropped")
            return
        if self.does_packet_delay(self.client_delay):
            print("Client ")
            self.delay_by_seconds(self.client_delay_time);
        self.chart.increment_chart_param("client_packet_sent")
        print("From Line 137 - Sending Message to Server: ", message, self.target_ip, self.target_port)
        self.proxy_socket.sendto(message,(self.target_ip, self.target_port) )

    def does_packet_delay(self, delay_chance: float) -> bool:
        """
        Determines if packet should be delayed

        @param delay_chance: probability of packet being delayed
        @return: True if packet should be delayed, False otherwise
        """
        if random.random() < delay_chance:
           return True
        return False

    def does_packet_drop(self, delay_chance: float) -> bool:
        """
        Determines if packet should be dropped

        @param delay_chance: probability of packet being dropped
        @return: True if packet should be dropped, False otherwise
        """
        if random.random() < delay_chance:
            return True
        return False

    def delay_by_seconds(self, delay_time: str) -> None:
        """
        Delays packet send by milliseconds

        @param delay_time: range of delay time in milliseconds
        """
        if "-" in delay_time:
            lower, upper = delay_time.split("-")
            delay = random.randrange(int(lower), int(upper)) if valid_fixed_or_range_number(lower) and valid_fixed_or_range_number(upper) else 0
            print(f"Packet is delayed by {delay} second(s)")
            time.sleep(delay/1000)
        else:
            delay = int(delay_time)
            print(f"Packet is delayed by {delay} millisecond(s)")
            time.sleep(delay/1000)

    def is_server(self, ip, port) -> bool:
        if ip == self.target_ip and port == self.target_port:
            return True
        return False

    def monitor_user_input(self):
            """
            Monitors user input to change proxy parameters dynamically.
            """
            while self.monitor_thread_condition:
                try:
                    if self.display_options:
                        print("CMD (e.g., 'client_drop 0.2', 1, 2, or q): \n")
                    user_input = input().strip().split()

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
                        elif command == "3":
                            self.monitor_thread_condition = False
                        elif command == "o":
                            self.display_options = not self.display_options
                        elif  command == "q":
                            self.proxy_socket.close()
                            exit()
                    elif len(user_input) == 2:
                        param, value = user_input
                        self.update_parameter(param, value)
                    elif len(user_input) == 5:
                        c_drop, s_drop, c_delay, s_delay, delay_time = user_input
                        self.client_drop = int(c_drop) / Proxy.HUNDRED
                        self.server_drop = int(s_drop) / Proxy.HUNDRED
                        self.client_delay = int(c_delay) / Proxy.HUNDRED
                        self.server_delay = int(s_delay) / Proxy.HUNDRED
                        self.client_delay_time = delay_time
                        self.server_delay_time = delay_time
                    else:
                        print("Invalid command. Please enter a valid command.")
                except ValueError:
                    print("Invalid value. Please enter a valid number.")
                except Exception as e:
                    print(f"Error: {e}")

    def close(self):
        """
        Closes the proxy server and joins the monitor thread.
        """
        print("Geneating Chart")
        self.chart.generate_client_chart()
        self.chart.generate_server_chart()
        self.proxy_socket.close()
        exit()


    def update_parameter(self, param: str, value: str) -> None:
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

    def start_monitoring(self) -> None:
        """
        Starts the user input monitoring thread.
        """
        self.monitor_thread.start()
