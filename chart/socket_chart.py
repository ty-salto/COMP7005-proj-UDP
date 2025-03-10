import datetime
import matplotlib.pyplot as plt
from matplotlib.axis import Axis

import matplotlib.ticker  as ticker


class SocketChart:
    def __init__(self, socket_name: str):
        self.socket_name = socket_name
        self.packet_received = 0
        self.packet_sent = 0
        self.packet_dropped = 0
        self.packet_retransmitted = 0
        self.time_start = datetime.datetime.now()
        self.time_elapsed = []
        self.info = {}
        self.initialize_chart_params()

    def display_current_stats(self):
        print(f"Received: {self.packet_received}")
        print(f"Sent: {self.packet_sent}")
        print(f"Dropped: {self.packet_dropped}")
        print(f"Retransmitted: {self.packet_retransmitted}")


    def initialize_chart_params(self):
            self.info = {}
            for param in [
                "packet_received", "packet_sent", "packet_dropped", "packet_retransmitted"

            ]:
                self.info[param] = []

    def increment_chart_param(self, param: str):
        """ DEPRECATED"""
        if hasattr(self, param):
            setattr(self, param, getattr(self, param) + 1)

            # Store the time elapsed and new value
            elapsed_time = (datetime.datetime.now() - self.time_start).total_seconds()
            self.time_elapsed.append(elapsed_time)
            if param == "packet_received":
                self.info[param].append(getattr(self, param)/self.packet_sent)
            elif param == "packet_retransmitted":
                self.info[param].append(getattr(self, param))
            else:
                self.info[param].append(getattr(self, param))
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{param}'")

    def create_timestamp(self):
        """
        Create a timestamp for the current time. These will be used for some x-values in the chart.
        """
        elapsed_time = (datetime.datetime.now() - self.time_start).total_seconds()
        self.time_elapsed.append(elapsed_time)

    def increment_packet_sent(self):
        self.create_timestamp()
        self.packet_sent += 1
        self.info["packet_sent"].append(self.packet_sent)

    def increment_packet_dropped(self):
        self.create_timestamp()
        self.packet_dropped += 1
        self.info["packet_dropped"].append(self.packet_dropped)

    def append_retransmit_packet(self, amount: float, limit: int):
        """Append the retransmit ratio to the chart data."""
        self.create_timestamp()
        self.packet_retransmitted += amount
        self.info["packet_retransmitted"].append(amount)

    def increment_packet_received(self):
        """Append the received ratio to the chart data."""
        self.create_timestamp()
        self.packet_received += 1
        if self.packet_sent <= 0:
            self.info["packet_received"].append(0)
        else:
            self.info["packet_received"].append(self.packet_received/self.packet_sent)

    def generate_chart(self):
        self.display_current_stats()
        figure, axis = plt.subplots(2, 2, figsize=(12, 8))
        figure.suptitle(f"{self.socket_name} Packet Analysis", fontsize=14)
        print(self.info.items())

        # Packets Sent
        axis[0, 0].plot(self.time_elapsed[:len(self.info["packet_sent"])], self.info["packet_sent"], label="Sent")
        axis[0, 0].set_title("Packets Over Time", fontsize=10)
        axis[0, 0].set_xlabel("Time Elapsed")
        axis[0, 0].set_ylabel("Packets Sent")
        axis[0, 0].set_ylim(0, max(self.info["packet_sent"])+1)


        # ACK RATIO
        axis[0, 1].plot(self.time_elapsed[:len(self.info["packet_received"])], self.info["packet_received"], label="Received")
        axis[0, 1].set_title("Packets Ratio Over Time", fontsize=10)
        axis[0, 1].set_ylim(0, 1)
        axis[0, 1].set_xlabel("Time Elapsed")
        axis[0, 1].set_ylabel("ACK-Ratio")

        # Packets Retransmitted

        axis[1, 0].scatter(self.info["packet_sent"][:len(self.info["packet_retransmitted"])], self.info["packet_retransmitted"], label="Retransmitted")
        axis[1, 0].set_ylim(0, 10)
        axis[1, 0].set_title("Packets Retransmitted Over Time", fontsize=10)  # Smaller title
        axis[1, 0].set_xlabel("Packet")
        axis[1, 0].set_ylabel("Packets Retransmitted")

        # Packets Dropped
        axis[1, 1].plot(self.time_elapsed[:len(self.info["packet_dropped"])], self.info["packet_dropped"], label="Dropped")
        axis[1, 1].set_title("Packets Dropped Over Time", fontsize=10)  # Smaller title
        axis[1, 1].set_xlabel("Time Elapsed")
        axis[1, 1].set_ylabel("Packets Dropped")

        plt.tight_layout()  # Adjust spacing
        plt.show()
