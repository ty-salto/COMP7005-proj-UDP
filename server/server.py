import socket
from chart.socket_chart import SocketChart
from ast import increment_lineno
class Server:
    FIRST_INDEX, SECOND_INDEX = (0,1)

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None
        self.uid_seq_dict = {}
        self.chart = SocketChart("Server")


    def server_init(self):
        print("SYSTEM INFO:")
        print("\t-Server Initialize...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        print("\t-Server Binding...")
        self.server_socket.bind((self.server_ip, self.server_port))

        return self.FIRST_INDEX


    def server_listen(self):
        try:
            print("\t-Waiting..")
            print("Current Stats : ", self.uid_seq_dict)
            client_packet = self.server_socket.recvfrom(1024)
            return self.FIRST_INDEX, client_packet# return tuple [data, client_addr]
        except KeyboardInterrupt:
            return self.SECOND_INDEX



    def server_receive(self, client_packet):
        print("\t-Server Receiving...")

        packet, client_addr = client_packet
        flag, uid, seq, message = packet.decode().split('|', 3)

        print(f"\t\tSender IP:{client_addr[0]}\n\t\tSender Port:{client_addr[1]}")
        print(f"\t\tPacket Data:")
        
        if uid in self.uid_seq_dict and seq in self.uid_seq_dict.get(uid):
            print(f"seq({seq}) Exist!")
        else:
            print(f"\t\t\t{client_packet[0].decode()}")
        self.chart.increment_packet_received()
        return self.FIRST_INDEX, packet, client_addr

    def server_response(self, newPacket, ip, port):
        print(f"\t-Server Responding...\n\t\tip: {ip}\n\t\tport: {port}...")
        self.server_socket.sendto(newPacket.encode(), (ip,port))
        self.chart.increment_packet_sent()
        return self.FIRST_INDEX

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
    def server_packet_process(self, packet: str, client_addr: tuple):
        print(f"\t-Server Packet processing")
        flag, uid, seq, message = packet.decode().split('|', 3)
        ip, port = client_addr

        if int(flag) == 12: # reset
            print("\t\tRST Flag...")
            self.uid_seq_dict[uid] = [seq]
        elif int(flag) == 4:
            print("\t\tSEQ Flag...")
            seq_list = self.uid_seq_dict.get(uid)

            if seq not in seq_list:
                seq_list.append(seq)

        ack_packet = f"2|{uid}|{seq}|"
        return self.FIRST_INDEX, ack_packet, ip, port
    
    def server_close(self):
        if self.server_socket:
            print("\t\t-Closing server socket...")
            self.server_socket.close()
            self.server_socket = None  # Ensure it's not used again
            print("\t-Server Socket Closed.")
        
