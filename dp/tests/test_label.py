import unittest
from unittest.mock import patch, Mock
import numpy as np


class TestLabel(unittest.TestCase):
    def setUp(self):
        self.Ty = 1375

    @patch('os.environ.get', side_effect=lambda *args: 1375 if args[0] == 'Ty' else None)
    def test_insert_ones(self, env_mock):
        from label import insert_ones
        arr1 = insert_ones(np.zeros((1, self.Ty)), 9700)
        insert_ones(arr1, 4251) [0, :]
        self.assertEqual((0.0, 1.0, 1.0, 0.0), (arr1[0][1333], arr1[0][1334], arr1[0][634], arr1[0][635]))

    def test_random(self):
        print(np.random.randint(10, size=3))
