import unittest
from .model import model


class ModelTest(unittest.TestCase):
    def setUp(self):
        self.Tx = 5511
        self.n_freq = 101

    def test_summary(self):
        m = model(input_shape=(self.Tx, self.n_freq))
        print(m.to_json(indent=4))
