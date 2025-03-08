import socket
import math
import select

from utils.helper import packet_uid_generator

class Client:
    FIRST_INDEX, SECOND_INDEX = (0,1)
    RETRANSMIT_COUNT_LIMIT = 10

    def __init__(self, client_ip, client_port):

        self.client_ip = client_ip
        self.client_port = client_port
        self.message_buffer_dict = {}
        self.poll = select.poll()
        self.retransmit_count = 0


    def client_init(self):
        print("Client Initialize...")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        print("Type your message and press Enter. Type 'exit' to quit.")
        return self.FIRST_INDEX
    
    def client_message(self):
        message = input("You: ")
        
        if message.lower() == "exit":
            print("Closing connection...")
            return self.SECOND_INDEX
        
        return  self.FIRST_INDEX ,message

        
    def client_send(self):
        print("Client Sending...")

        # always the first uid
        # works only for python 3.7+ where dictionary is ordered by first input
        ##uid_to_send = list(self.message_buffer_dict.keys())[0] 
        self.uid_to_send = next(iter(self.message_buffer_dict.keys()))

        print(self.message_buffer_dict[self.uid_to_send])
        
        packet_to_send= self.message_buffer_dict[self.uid_to_send][0][1]

        self.client_socket.sendto(packet_to_send.encode(), (self.client_ip, self.client_port))
        
        return self.FIRST_INDEX


    def client_receive(self):
        print("Client Receiving...")

        self.poll.register(self.client_socket, select.POLLIN)

        events = self.poll.poll(300) ## in miliseconds

        if not events:
            if self.retransmit_count < self.RETRANSMIT_COUNT_LIMIT:
                print("Timeout: Retransmit")
                self.retransmit_count += 1
                return self.FIRST_INDEX
            else:
                self.message_buffer_dict.pop(self.uid_to_send)
                self.retransmit_count = 0
                return self.SECOND_INDEX

        data, client_addr = self.client_socket.recvfrom(1024)

        # needs to change to parse the message receive
        uid_receive = next(iter(self.message_buffer_dict.keys())) 
        packet_count = len(self.message_buffer_dict[uid_receive])
        packet_seq= self.message_buffer_dict[uid_receive][0][0]


        print(f"Received ({client_addr}): {data.decode()}")

        for i in range(0,packet_count):
            if self.message_buffer_dict[uid_receive][i][0] == packet_seq:
                self.message_buffer_dict[uid_receive].pop(i)

                if len(self.message_buffer_dict[uid_receive]) == 0:
                    self.message_buffer_dict.pop(uid_receive)
                    return self.SECOND_INDEX
                
                return self.FIRST_INDEX


        return self.SECOND_INDEX
    
    def client_closing(self):
        print("Closing client socket...")
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
        print("Processing Packets to send...")
        
        message_len = len(message)
        packet_count = math.ceil(message_len/255) if message_len != 0 else 0
        prev_seq = 0
        message_uid = packet_uid_generator()

        if packet_count == 0:
            packet_struct = f"12|{message_uid}|{prev_seq}|"
            self.message_buffer_dict[message_uid] = [(0, packet_struct)]
            return self.FIRST_INDEX
            
        self.message_buffer_dict[message_uid] = []
        
        for i in range(0, packet_count):
            curr_seq = prev_seq + min(255, message_len - prev_seq)
            curr_packet_message = message[prev_seq:curr_seq]

            flag = 12 if prev_seq == 0 else 4
            packet_struct = f"{flag}|{message_uid}|{curr_seq}|{curr_packet_message}"

            self.message_buffer_dict[message_uid].append((curr_seq, packet_struct))

            prev_seq = curr_seq
        
        return self.FIRST_INDEX




