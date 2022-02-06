import unittest

class TestGrodibExtraction(unittest.TestCase):
    def test_list_int(self):
        data = [1, 2, 3]
        result = 6 
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()