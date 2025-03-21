import socket
import math
import select
import threading
import queue

from chart.socket_chart import SocketChart
from utils.helper import packet_uid_generator

class Client:
    FIRST_INDEX, SECOND_INDEX, THIRD_INDEX = (0,1,2)
    RETRANSMIT_COUNT_LIMIT = 10
    TIMEOUT_TIME = 300

    def __init__(self, client_ip, client_port):

        self.client_ip = client_ip
        self.client_port = client_port
        self.message_buffer_dict = {}
        self.poll = select.poll()
        self.retransmit_count = 0
        self.chart = SocketChart("Client")


        #self.received_message_queue = queue.Queue()

        """ Start a separate thread to continuously receive messages """
        self.receive_thread = threading.Thread(target=self.client_receive, daemon=True)
        self.receive_thread.start()

        self.message_removed_event = threading.Event()


    def client_init(self):
        print("Client Initialize...")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        self.poll.register(self.client_socket, select.POLLIN)
        print("Type your message and press Enter. Type 'exit' to quit.")
        return self.FIRST_INDEX

    def client_message(self):
        message = input("You: ")

        print("\tSYSTEM INFO:")

        if message.lower() == "g":
            self.chart.generate_client_chart()
        if message.lower() == "exit":
            print("\t\t-Closing connection...")
            return self.SECOND_INDEX

        return  self.FIRST_INDEX ,message


    def client_send(self):
        print("\t\t-Client Sending...")

        # always the first uid
        # works only for python 3.7+ where dictionary is ordered by first input
        self.uid_to_send = next(iter(self.message_buffer_dict.keys()))

        print(f"\t\t\tuid:{self.uid_to_send}; seq:{self.message_buffer_dict.get(self.uid_to_send)[0][0]}")

        packet_to_send = self.message_buffer_dict[self.uid_to_send][0][1]

        self.client_socket.sendto(packet_to_send.encode(), (self.client_ip, self.client_port))
        self.chart.increment_packet_sent()


        self.message_removed_event.wait()  # Wait until a new message is available
        # Reset the event before waiting
        self.message_removed_event.clear()

        return self.FIRST_INDEX


    def client_receive(self):
        while True:
            if self.message_buffer_dict:
                events = self.poll.poll(self.TIMEOUT_TIME) ## in miliseconds

                if not events:
                    if self.retransmit_count < self.RETRANSMIT_COUNT_LIMIT:

                        self.chart.increment_packet_dropped()
                        print(f"\t\t-Timeout: Retransmit (count:{self.retransmit_count + 1})")
                        self.retransmit_count += 1

                        self.uid_to_send = next(iter(self.message_buffer_dict.keys()))

                        print(f"\t\t\tuid:{self.uid_to_send}; seq:{self.message_buffer_dict.get(self.uid_to_send)[0][0]}")

                        packet_to_send = self.message_buffer_dict[self.uid_to_send][0][1]


                        #TODO: Dropping means it shoiuld equally retransmit This should be the spot to count the retransmit
                        self.client_socket.sendto(packet_to_send.encode(), (self.client_ip, self.client_port))
                        if self.retransmit_count < self.RETRANSMIT_COUNT_LIMIT:
                            self.chart.increment_packet_sent()
                        #return self.FIRST_INDEX
                    else:
                        self.message_buffer_dict.pop(self.uid_to_send)
                        self.chart.append_retransmit_packet(self.retransmit_count, self.RETRANSMIT_COUNT_LIMIT)
                        self.retransmit_count = 0
                        self.message_removed_event.set()
                        #return self.SECOND_INDEX
                else:
                    recv_packet = self.client_socket.recvfrom(1024)
                    self.client_packet_receive(recv_packet)


            #return self.THIRD_INDEX, recv_packet



    def client_closing(self):
        print("\t\t-Closing client socket...")
        self.chart.generate_client_chart()
        self.client_socket.close()

    '''
        Packet structure:
        <flag:int>|<UID:8bytes/16hex char>|<seq:0-999,999>|<message:255char>

        flgs:
        1000 - rst -> Reset Flag
        0100 - seq -> Sequence Flag
        0010 - ack -> Acknowledge Flag
        0001 - fin -> Finish/End Flag


        UID:
        Random generated 8 bytes value in 16 hex character

        seq:
        Packet sequence number based on the message length

        message:
        The message being transmitted with max size of 255 character per packet

        Total packet sturcture size (| included):
        Min: 21 character => 21 bytes (sending blank message allowed)
        Max: 282 character => 282 bytes
    '''
    def client_packet_to_send(self, message):
        print("\t\t-Processing Packets to send...")

        message_len = len(message)
        packet_count = math.ceil(message_len/255) if message_len != 0 else 0
        prev_seq = 0
        message_uid = packet_uid_generator()

        # sends empty message
        if packet_count == 0:
            packet_struct = f"12|{message_uid}|{prev_seq}|"
            self.message_buffer_dict[message_uid] = [(0, packet_struct)]
            return self.FIRST_INDEX

        # Initialize a packet list based from th message uid
        self.message_buffer_dict[message_uid] = []

        # divides the packets if the message length is more than 255 char
        for i in range(0, packet_count):
            curr_seq = prev_seq + min(255, message_len - prev_seq)
            curr_packet_message = message[prev_seq:curr_seq]

            flag = 12 if prev_seq == 0 else 4
            packet_struct = f"{flag}|{message_uid}|{curr_seq}|{curr_packet_message}"

            self.message_buffer_dict[message_uid].append((curr_seq, packet_struct))

            prev_seq = curr_seq

        return self.FIRST_INDEX

    def client_packet_receive(self, recv_packet):
        packet, server_addr = recv_packet
        flag, uid, seq, message = packet.decode().split('|', 3)

        #packet_count = len(self.message_buffer_dict[uid])

        if int(flag) == 2:
            self.chart.increment_packet_received()

            if uid in self.message_buffer_dict:
                buffer_packets = self.message_buffer_dict[uid]

                for i in range(len(buffer_packets)):
                    if buffer_packets[i][0] == int(seq):
                        print("\t\t-Removing seq...")
                        buffer_packets.pop(i)

                        #TODO: Retransmit is in the wrong place. this is for successful transmission
                        self.chart.append_retransmit_packet(self.retransmit_count, self.RETRANSMIT_COUNT_LIMIT)
                        # reset retranmission count if ack received for the seq.
                        self.retransmit_count = 0
                        print(f"\t\t\tACK received({server_addr[0]}): flag:{flag}; uid:{uid}; seq:{seq}")
                        break

                if not buffer_packets:
                    self.message_buffer_dict.pop(uid)
                    print("\t\t-Deleting uid...")
                    self.message_removed_event.set()
                # else:
                #     return self.SECOND_INDEX


        # return self.FIRST_INDEX
