import sys
sys.path.append("test/mock")
import ev3_mock as ev3 # Simulated Test Environment
#import ev3dev.ev3 as ev3 # Live Environment

#from sorter_app.ev3_scheduler_socket import SchedulerSocket as ss # Live Environment
from scheduler_socket_mock import SchedulerSocket as ss

from time import perf_counter
import time
import datetime as dt
import signal

class Scheduler(object):

    #Scheduler variables
    globals()["tasks_were_completed"] = False

    multiple_dispenser_motor = ev3.LargeMotor('outA')
    single_dispenser_motor = ev3.LargeMotor('outB')
    card_pusher_motor = ev3.MediumMotor('outC')

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



    def single_dispenser(self, sd, position):
        # Updating Symbol Table to Move One Cycle
        globals()['front_pos'] = position - 50
        # Setting the position to the new target
        position = globals()['front_pos']
        # Running one Cycle to the targeted position.
        sd.run_to_abs_pos(position_sp=position, speed_sp=40)
        time.sleep(2)
        return position

    # Tænk på at få den til at køre på worst time af et kort et antal gange
    def dispense_one_card(self, sd):
        for x in range(6):
            if not (ss.socket_if_card(self)):
                self.single_dispenser(sd, front_pos)

    def get_card_placement(self):
        card = 1
        card = saw_card
        if card == 1:
            return ss.socket_get_placement(self)


    def position_cc(self, card_placement):
        if saw_card == 1:
            ss.socket_place_cc(self, card_placement)

    def push_card(self, cp, position):
        if saw_card == 1:
            # Updating Symbol Table to Move One Cycle
            globals()['piston_pos'] = position + 360
            # Setting the position to the new target
            position = globals()['piston_pos']
            # Running one Cycle to the targeted position.
            cp.run_to_abs_pos(position_sp=position, speed_sp=400)
            time.sleep(5)
            return position

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
        self.calibrate_machine(self.multiple_dispenser_motor, self.single_dispenser_motor, self.card_pusher_motor)
        minor_cycle_duration = 130
        second_scheduler = 5
        signal.signal(signal.SIGALRM, interrupt_handler)
        
        while True:
            signal.alarm(minor_cycle_duration)

            if second_scheduler == 5: #Only runs this every 5 minor cycles
                multiple_dispenser(multiple_dispenser_motor, back_pos) #computation time (CT): 11
                second_scheduler = 0
            dispense_one_card(single_dispenser_motor) #CT: 37
            card_placement = get_card_placement() #CT: 10
            position_cc(card_placement) #CT: 33
            push_card(piston_pos) #CT: 5

            wait_for_interrupt()
            second_scheduler += 1


    def test_runner(self):
        globals()['saw_card'] = 1
        self.calibrate_machine(self.multiple_dispenser_motor, self.single_dispenser_motor, self.card_pusher_motor)
        self.multiple_dispenser(self.multiple_dispenser_motor, back_pos)
        self.dispense_one_card(self.single_dispenser_motor)
        card_placement = self.get_card_placement()
        print(card_placement)
        self.position_cc(card_placement)
        self.push_card(self.card_pusher_motor, piston_pos)

    def pretty_print_CE(self, period_start_time_p, minor_cycle_p, current_cycle_p):
        print("This cycle: ")
        print("Period start: " + str(period_start_time_p))
        print("Minor Cycle: " + str(minor_cycle_p))
        print("Currenct Cycle: " + str(current_cycle_p))
        print("Lower bound: " + str(period_start_time_p + minor_cycle_p * current_cycle_p))
        print("Upper bound: " + str(period_start_time_p + minor_cycle_p * (current_cycle_p + 1)))

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
    schd.test_runner()
