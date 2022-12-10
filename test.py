import unittest
from app import score, HOLE_IN_ONE

class PlayNineTests(unittest.TestCase):

    def test_score(self):
        # Nothing Special       0  1  2  -5           0  0  0  0
        result = score([0, 1, 2, HOLE_IN_ONE, 1, 1, 2, 2])
        self.assertEqual(result, -2)

        # Hole in One Pair      1  2  -5           -5           0  0  0  0
        result = score([1, 2, HOLE_IN_ONE, HOLE_IN_ONE, 3, 3, 4, 4])
        self.assertEqual(result, -7)
        
        # Matching 4 Cards      3  1  0  0  6  5  0  0: -10 Bonus
        result = score([3, 1, 5, 5, 6, 5, 5, 5])
        self.assertEqual(result, 5)

        # Matching 4 Cards      4  1  0  0  2  4  0  0: -10 Bonus
        result = score([4, 1, 4, 4, 2, 4, 4, 4])
        self.assertEqual(result, 1)

        # Matching 6 Cards      0  0  0  0  0  0  1  2: -15 Bonus
        result = score([4, 4, 4, 4, 4, 4, 1, 2])
        self.assertEqual(result, -12)

        # Matching 8 Cards -20 Bonus
        result = score([6] * 8)
        self.assertEqual(result, -20)
        
        #                       -5           -5           -5           -5           5  1  6  3: -10 Bonus
        result = score([HOLE_IN_ONE, HOLE_IN_ONE, HOLE_IN_ONE, HOLE_IN_ONE, 5, 1, 6, 3])
        self.assertEqual(result, -15)

if __name__ == '__main__':
    unittest.main()
