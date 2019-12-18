import unittest as ut
import sys
sys.path.append("sorter_app")
sys.path.append("test/mock")
import ev3_mock as ev3 # Simulated Test Environment
from ev3_cc import CardCollector

class TestCC(ut.TestCase):
    def setUp(self):
        self.ev3_cc = CardCollector()


if __name__ == '__main__':
    ut.main()
    