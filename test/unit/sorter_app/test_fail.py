import unittest as ut
import sys
sys.path.append("sorter_app")
from calc import Calculate

class TestCalculate(ut.TestCase):
    def setUp(self):
        self.calc = Calculate()

    def test_add_return_false(self):
        self.assertEqual(4, self.calc.add(2,2))
                   
    def test_add_return_correct(self):
        self.assertEqual(5, self.calc.add(2,2))


if __name__ == '__main__':
    ut.main()
    
