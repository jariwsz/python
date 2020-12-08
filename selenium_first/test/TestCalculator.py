import unittest
from calculators import Calculator


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('This will run before class.')

    @classmethod
    def tearDownClass(cls):
        print('This will run after class.')


    def setUp(self):
        print('This will run before every method.')

    def tearDown(self):
        print("This will run after every method.")


    def test_add(self):
        self.assertEqual(0, Calculator.add(self, 0, 0))
        self.assertEqual(30, Calculator.add(self, 10, 20))
        self.assertEqual(100, Calculator.add(self, 50, 50))

    def test_sub(self):
        self.assertEqual(0, Calculator.sub(self, 0, 0))
        self.assertEqual(30, Calculator.sub(self, 50, 20))
        self.assertEqual(100, Calculator.sub(self, 150, 50))


if __name__ == '__main__':
    unittest.main()
