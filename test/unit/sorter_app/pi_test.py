import unittest as ut
import sys
sys.path.append("sorter_app")
from pi import RasPi
from PIL import Image

class TestPi(ut.TestCase):
    def setUp(self):
        self.pi = RasPi()

    def test(self):
        start_path = "test/unit/sorter_app/start_rez.jpg"
        end_path = "test/unit/sorter_app/end_rez.jpg"
        self.pi.resizer(start_path, end_path)
        im = Image.open(end_path)
        width, height = im.size
        self.assertEqual(width, 224, msg="Width is not the same on Resize Function")
           

if __name__ == '__main__':
    ut.main()
    