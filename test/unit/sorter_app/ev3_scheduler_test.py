import unittest as ut
import sys
sys.path.append("sorter_app")
sys.path.append("test/mock")
import ev3_mock as ev3 # Simulated Test Environment
from ev3_scheduler import Scheduler

class TestScheduler(ut.TestCase):
    def setUp(self):
        self.ev3_scheduler = Scheduler()

    def test_dispense_one_card(self):
        # Defining Motors
        single_dispenser_motor = ev3.LargeMotor('outB')

        # Defining Attributes
        position = 0

        # Running Methods
        self.ev3_scheduler.dispense_one_card(single_dispenser_motor)

    def test_multiple_dispenser(self):
        # Defining Motors
        multiple_dispenser_motor = ev3.LargeMotor('outA')

        # Defining Attributes
        position = 0

        # Running Methods
        position = self.ev3_scheduler.multiple_dispenser(multiple_dispenser_motor, position)
        position = self.ev3_scheduler.multiple_dispenser(multiple_dispenser_motor, position)
        self.assertEqual(multiple_dispenser_motor.position, -2000, msg="Position for MD is not -2000")

    def test_single_dispenser(self):
        # Defining Motors
        single_dispenser_motor = ev3.LargeMotor('outB')

        # Defining Attributes
        position = 0

        # Running Methods
        position = self.ev3_scheduler.single_dispenser(single_dispenser_motor, position)
        position = self.ev3_scheduler.single_dispenser(single_dispenser_motor, position)
        position = self.ev3_scheduler.single_dispenser(single_dispenser_motor, position)
        position = self.ev3_scheduler.single_dispenser(single_dispenser_motor, position)
        self.assertEqual(single_dispenser_motor.position, -200, msg="Position for SD is not -200")

    def test_calibrate(self):
        # Defining Motors
        multiple_dispenser_motor = ev3.LargeMotor('outA')
        single_dispenser_motor = ev3.LargeMotor('outB')
        card_pusher_motor = ev3.MediumMotor('outC')

        # Running Methods
        self.ev3_scheduler.calibrate_machine(multiple_dispenser_motor, single_dispenser_motor, card_pusher_motor)

        # Checking and Testing
        self.assertEqual(multiple_dispenser_motor.position, 0, msg="Position for MD is not 0")
        self.assertEqual(single_dispenser_motor.position, 0, msg="Position for SD is not 0")
        self.assertEqual(card_pusher_motor.position, 0, msg="Position for CP is not 0")

    def test_all_together(self):
        schd = Scheduler()
        schd.test_runner()

    
if __name__ == '__main__':
    ut.main()
    