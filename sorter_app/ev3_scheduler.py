import sys
sys.path.append("test/mock")
import ev3_mock as ev3 # Simulated Test Environment
#import ev3dev.ev3 as ev3 # Live Environment
from time import perf_counter
import time
import socket
import datetime as dt
import signal

class Scheduler(object):

    #Scheduler variables
    globals()["tasks_were_completed"] = False

    multiple_dispenser_motor = ev3.LargeMotor('outA')
    single_dispenser_motor = ev3.LargeMotor('outB')
    card_pusher_motor = ev3.MediumMotor('outC')

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
    # UDP_server_socket.bind((local_IP, local_Port))

    # Set Postion of each Motor in Symboltable for global reference and updating.
    globals()['back_pos'] = 0
    globals()['front_pos'] = 0
    globals()['piston_pos'] = 0
    globals()['saw_card'] = 0
    globals()['current_cycle'] = 0

    def __init__(self):
        pass

    def calibrate_machine(self, md, sd, cp):
        position = 0
        print("Starting Calibration...")
        md.run_to_abs_pos(position_sp=position, speed_sp=1000)
        sd.run_to_abs_pos(position_sp=position, speed_sp=1000)
        cp.run_to_abs_pos(position_sp=position, speed_sp=400)
        time.sleep(30)
        md.run_to_abs_pos(position_sp=position, speed_sp=50)
        sd.run_to_abs_pos(position_sp=position, speed_sp=50)
        time.sleep(30)
        print("Calibrated")
        print("Place cards within 5 seconds...")
        time.sleep(5)
        print("Calibration done - starting")
        return


    def multiple_dispenser(self, md, position):
        # Updating Symbol Table to Move One Cycle
        globals()['back_pos'] = position - 1000
        # Setting the position to the new target
        position = globals()['back_pos']
        # Running one Cycle to the targeted position. // Optimiation, test with only symble table call
        md.run_to_abs_pos(position_sp=position, speed_sp=200)
        time.sleep(8)
        md.run_to_abs_pos(position_sp=position, speed_sp=50)
        time.sleep(3)
        return position



    def single_dispenser(self, position):
        # Updating Symbol Table to Move One Cycle
        globals()['front_pos'] = position - 50
        # Setting the position to the new target
        position = globals()['front_pos']
        # Running one Cycle to the targeted position.
        single_dispenser_motor.run_to_abs_pos(position_sp=position, speed_sp=40)
        time.sleep(2)
        return position

    # Tænk på at få den til at køre på worst time af et kort et antal gange
    def dispense_one_card(self):
        for x in range(6):
            if not check_if_card():
                single_dispenser(front_pos)

    def check_if_card(self):
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


    def get_card_placement(self):
        if saw_card == 1:
            msg_from_client = "REQUEST"
            bytes_to_send = str.encode(msg_from_client)
            buffer_size = 1024
            UDP_client_socket.sendto(bytes_to_send, pi_address_port)
            msg_from_server = UDP_client_socket.recvfrom(buffer_size)
            print("Card check upcode from the Rasberry Pi {}".format(msg_from_server[0]))
            return msg_from_server[0]


    def position_cc(self, card_placement):
        if saw_card == 1:
            bts = str.encode(card_placement)
            cc_UDP_client_socket.sendto(bts, cc_address_port)
            bytes_address_pair = cc_UDP_client_socket.recvfrom(buffer_size)  # Receives mesage back from card collector
            print("Connection Established")
            message = bytes_address_pair[0]  # Stores the message
            client_msg = "Message from Client:{}".format(message)

    def push_card(self, position):
        if saw_card == 1:
            # Updating Symbol Table to Move One Cycle
            globals()['piston_pos'] = position + 360
            # Setting the position to the new target
            position = globals()['piston_pos']
            # Running one Cycle to the targeted position.
            card_pusher_motor.run_to_abs_pos(position_sp=position, speed_sp=400)
            time.sleep(5)



    def dispense_at_least_5_cards(self):
        # Runs the dispenser enough to at least dispense 5 cards, worst case execution time of one card 5 times?
        # we need to base this on something and then this can be one big task, and talk about how this makes our system
        # slower since we need to base it on worst case execution time of up to 5 cards even though less may be dispensed
        for x in range(24):
            single_dispenser_motor(front_pos)
            check_if_card()
            if saw_card == 1:
                get_card_placement()
                # Send message to card collector
                bytes_address_pair = UDP_server_socket.recvfrom(buffer_size)
                print("Connection Established")
                message = bytes_address_pair[0]
                client_msg = "Message from Client:{}".format(message)
                if "OK" in client_msg:
                    push_card(piston_pos)


    # Runs when an interrupt happens. Might get some fault tolerance depending on what approach is best.
    def interrupt_handler(self, signum, frame):
        print('Signal handler called with signal', signum)
        if tasks_were_completed:
            globals()['tasks_were_completed'] = False
            globals()['current_cycle'] += 1
        else:
            print('Overran')

    def wait_for_interrupt(self):
        globals()['tasks_were_completed'] = True
        # Do nothing until the end of this cycle
        while(tasks_were_completed):
            time.sleep(0)

    def cyclic_executives(self):
        # Ensures machine always starts in the same state
        calibrate_machine(multiple_dispenser_motor, single_dispenser_motor, card_pusher_motor)
        minor_cycle_duration = 130
        second_scheduler = 5
        signal.signal(signal.SIGALRM, interrupt_handler)
        
        while True:
            signal.alarm(minor_cycle_duration)

            if second_scheduler == 5: #Only runs this every 5 minor cycles
                multiple_dispenser(multiple_dispenser_motor, back_pos) #computation time (CT): 11
                second_scheduler = 0
            dispense_one_card() #CT: 37
            card_placement = get_card_placement() #CT: 10
            position_cc(card_placement) #CT: 33
            push_card(piston_pos) #CT: 5

            wait_for_interrupt()
            second_scheduler += 1


    def test_runner(self):
        globals()['saw_card'] = 1
        #calibrate_machine()
        #multiple_dispenser(back_pos)
        #dispense_one_card()
        card_placement = get_card_placement()
        #print(card_placement)
        
        #position_cc(card_placement)
        push_card(piston_pos)

    def pretty_print_CE(self, period_start_time_p, minor_cycle_p, current_cycle_p):
        print("This cycle: ")
        print("Period start: " + str(period_start_time_p))
        print("Minor Cycle: " + str(minor_cycle_p))
        print("Currenct Cycle: " + str(current_cycle_p))
        print("Lower bound: " + str(period_start_time_p + minor_cycle_p * current_cycle_p))
        print("Upper bound: " + str(period_start_time_p + minor_cycle_p * (current_cycle_p + 1)))
        
    #test_runner()
    #print("fuck")

    def take_time(self):
        log = ""
        f = open("cancer_collector.txt", "a+")
        worst_case = 0
        for x in (range(20)):
            start_time = dt.datetime.now().timestamp()
            card_placement = get_card_placement()
            time_taken = dt.datetime.now().timestamp() - start_time
            log = log + str(time_taken) + "\n"
            
            print(str(x))

            if(time_taken > worst_case):
                worst_case = time_taken
            
        log += "Worst case was: " + str(worst_case)
        f.write(log)
        f.close()

if __name__ == '__main__':
    schd = Scheduler()
    #schd.cyclic_executives()
