import socket

class SchedulerSocket(object):
    # Sets the READY message, which means that the ev3 is ready to communicate with the PI
    msg_from_client = "READY"

    # Setting up clocal

    # Setting Up the Server Settings for EV3cc
    local_IP = "192.168.2.3"
    local_Port = 22222
    buffer_size = 1024

    # Settings Up
    bytes_to_send = str.encode(msg_from_client)
    pi_address_port = ("169.254.204.164", 22222)  # IP and Port of the Raspberry PI
    cc_address_port = ("192.168.2.4", 60000)  # IP + Port of the CC EV3, change when it has an actual address

    # Create a UDP socket at client side
    UDP_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    cc_UDP_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_server_socket.bind((local_IP, local_Port))
    def __init__(self):
        pass

    def socket_if_card(self):
        # Asks the Pi if there is card or not. Card:No_card
        # Timeout on 15 seconds
        UDP_client_socket.sendto(bytes_to_send, pi_address_port)
        msg_from_server = UDP_client_socket.recvfrom(buffer_size)
        msg = "Card check upcode from the Rasberry Pi {}".format(msg_from_server[0])
        print(msg)
        if ("b'card'" in msg):
            print("Read Card")
            globals()['saw_card'] = 1
            return True
        if ("not_card" in msg):
            print("Read Not Card")
            globals()['saw_card'] = 0
            return False

    def socket_get_placement(self):
        msg_from_client = "REQUEST"
        bytes_to_send = str.encode(msg_from_client)
        buffer_size = 1024
        UDP_client_socket.sendto(bytes_to_send, pi_address_port)
        msg_from_server = UDP_client_socket.recvfrom(buffer_size)
        print("Card check upcode from the Rasberry Pi {}".format(msg_from_server[0]))
        return msg_from_server[0]

    def socket_place_cc(self, card_placement):
        bts = str.encode(card_placement)
        cc_UDP_client_socket.sendto(bts, cc_address_port)
        bytes_address_pair = cc_UDP_client_socket.recvfrom(buffer_size)  # Receives mesage back from card collector
        print("Connection Established")
        message = bytes_address_pair[0]  # Stores the message
        client_msg = "Message from Client:{}".format(message)
        if "OK" in client_msg:
            return







