import datetime
import matplotlib.pyplot as plt

class SocketChart:
    def __init__(self, socket_name: str):
        self.socket_name = socket_name
        self.packet_received = 0
        self.packet_sent = 0
        self.packet_dropped = 0
        self.packet_retransmitted = 0
        self.success_ratio = []
        self.time_start = datetime.datetime.now()
        self.time_elapsed = []
        self.info = {}
        self.figure, self.axis = plt.subplots(2, 2, figsize=(12, 8))
        self.initialize_chart_params()

    def display_current_stats(self):
        print(f"Received: {self.packet_received}")
        print(f"Sent: {self.packet_sent}")
        print(f"Dropped: {self.packet_dropped}")
        print(f"Retransmitted: {self.packet_retransmitted}")


    def initialize_chart_params(self):
        """Initialize the chart parameters.
        Structure:
            {
                "packet_received": [],
                "packet_sent": [],
                "packet_dropped": [],
                "packet_retransmitted": []
            }
        Each value in the list will be mapped to a list of values like elapsed time or packets
        """
        self.info = {}
        for param in [
            "packet_received", "packet_sent", "packet_dropped", "packet_retransmitted"

        ]:
            self.info[param] = []


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
        print("from retrans", amount)
        self.info["packet_retransmitted"].append(amount)

    def increment_packet_received(self):
        """Append the received ratio to the chart data."""
        self.create_timestamp()
        self.packet_received += 1
        self.info["packet_received"].append(self.packet_received)
        if self.packet_sent <= 0:
            self.success_ratio.append(1)
        else:
            self.success_ratio.append(self.packet_received / self.packet_sent)

    def generate_packets_sent_chart(self, x, y):
        self.axis[x, y].plot(self.time_elapsed[:len(self.info["packet_sent"])], self.info["packet_sent"], label="Sent")
        self.axis[x, y].set_title("Packets Over Time", fontsize=10)
        self.axis[x, y].set_xlabel("Time Elapsed")
        self.axis[x, y].set_ylabel("Packets Sent")
        self.axis[x, y].set_ylim(0, max(self.info["packet_sent"])+1)

    def generate_success_ratio(self, x, y):
        self.axis[x,y].plot(self.time_elapsed[:len(self.info["packet_received"])], self.success_ratio, label="Received")
        self.axis[x,y].set_title("Packets Ratio Over Time", fontsize=10)
        self.axis[x,y].set_ylim(0, 1)
        self.axis[x,y].set_xlabel("Time Elapsed")
        self.axis[x,y].set_ylabel("Success Rate")

    def generate_retransmission_chart(self, x, y):
        self.axis[x, y].scatter(self.info["packet_sent"][:len(self.info["packet_retransmitted"])], self.info["packet_retransmitted"], label="Retransmitted")
        self.axis[x, y].set_ylim(0, 10)
        self.axis[x, y].set_title("Packets Retransmitted Over Time", fontsize=10)
        self.axis[x, y].set_xlabel("Packet")
        self.axis[x, y].set_ylabel("Packets Retransmitted")

    def generate_drop_chart(self, x, y):
        self.axis[x, y].plot(self.time_elapsed[:len(self.info["packet_dropped"])], self.info["packet_dropped"], label="Dropped")
        self.axis[x, y].set_title("Packets Dropped Over Time", fontsize=10)
        self.axis[x, y].set_xlabel("Time Elapsed")
        self.axis[x, y].set_ylabel("Packets Dropped")

    def generate_summary_table(self, x, y):
        """Generates a summary table displaying total packet statistics."""
        summary_data = {
            "Packets Sent": [self.packet_sent],
            "Successful Packets": [self.packet_received],
            "Packets Retransmitted": [self.packet_retransmitted],
            "Packets Dropped": [self.packet_dropped]
        }

        # Convert to table format
        table_data = [[key, value] for key, value in summary_data.items()]


        self.axis[x, y].axis("off")
        table = self.axis[x, y].table(cellText=table_data, colLabels=["Metric", "Total"], loc="center", cellLoc="center")

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.2)

    def generate_client_chart(self):
        self.generate_summary_table(0,0)
        self.generate_packets_sent_chart(0,1)
        self.generate_success_ratio(1,0)
        self.generate_retransmission_chart(1,1)
        plt.tight_layout()
        plt.show()

    def generate_server_chart(self):
        self.generate_summary_table(0,0)
        self.generate_packets_sent_chart(0,1)
        self.generate_drop_chart(1,1)
        self.axis[1,0].axis("off")
        plt.tight_layout()
        plt.show()
