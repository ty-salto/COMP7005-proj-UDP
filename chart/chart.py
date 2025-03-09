import datetime
import matplotlib.pyplot as plt

class Chart:
    def __init__(self):
        self.client_packet_received = 0
        self.client_packet_sent = 0
        self.client_packet_dropped = 0
        self.client_packet_retransmitted = 0
        self.server_packet_sent = 0
        self.server_packet_received = 0
        self.server_packet_dropped = 0
        self.server_packet_retransmitted = 0
        self.time_start = datetime.datetime.now()
        self.time_elapsed = []  # Store elapsed time
        self.server_data = {}
        self.client_data = {}
        self.initialize_chart_params(True)
        self.initialize_chart_params(False)

    def display_current_stats(self):
        print("Client Stats:")
        print(f"Received: {self.client_packet_received}")
        print(f"Sent: {self.client_packet_sent}")
        print(f"Dropped: {self.client_packet_dropped}")
        print(f"Retransmitted: {self.client_packet_retransmitted}")

        print("\nServer Stats:")
        print(f"Received: {self.server_packet_received}")
        print(f"Sent: {self.server_packet_sent}")
        print(f"Dropped: {self.server_packet_dropped}")
        print(f"Retransmitted: {self.server_packet_retransmitted}")

        print("\nTime Stats:")
        print(f"Start Time: {self.time_start}")
        print(f"Elapsed Time: {self.time_elapsed}")

    def initialize_chart_params(self, is_server: bool):
        if is_server:
            self.server_data = {}
            for param in [
                "server_packet_dropped", "server_packet_sent", "server_packet_received", "server_packet_retransmitted"
            ]:
                self.server_data[param] = []
        else:
            self.client_data = {}
            for param in [
                "client_packet_received", "client_packet_sent", "client_packet_dropped", "client_packet_retransmitted"
            ]:
                self.client_data[param] = []

    def increment_chart_param(self, param: str):
        if hasattr(self, param):
            setattr(self, param, getattr(self, param) + 1)

            # Store the time elapsed and new value
            elapsed_time = (datetime.datetime.now() - self.time_start).total_seconds()
            self.time_elapsed.append(elapsed_time)

            # Track the updated values
            if param in self.server_data:
                self.server_data[param].append(getattr(self, param))
            elif param in self.client_data:
                self.client_data[param].append(getattr(self, param))
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{param}'")

    def generate_server_chart(self):
        plt.figure(figsize=(8, 5))
        for param, values in self.server_data.items():
            plt.scatter(self.time_elapsed[:len(values)], values, label=param)

        plt.xlabel("Time Elapsed (seconds)")
        plt.ylabel("Packet Count")
        plt.title("Server Packet Activity Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    def generate_client_chart(self):
        plt.figure(figsize=(8, 5))
        for param, values in self.client_data.items():
            plt.scatter(self.time_elapsed[:len(values)], values, label=param)

        plt.xlabel("Time Elapsed (seconds)")
        plt.ylabel("Packet Count")
        plt.title("Client Packet Activity Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()


# chart = Chart()

# # Simulating some increments over time
# import time
# for _ in range(10):
#     time.sleep(1)
#     chart.increment_chart_param("client_packet_received")
#     chart.increment_chart_param("server_packet_sent")

# # Generate charts
# chart.generate_server_chart()
# chart.generate_client_chart()
