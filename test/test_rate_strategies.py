# test_rate_strategies.py

import unittest

from paystation.domain import linear_rate_strategy


class TestLinearRate(unittest.TestCase):

    def test_correct_value_for_100_cents(self):
        lrs = linear_rate_strategy
        self.assertEqual(100 // 5 * 2, lrs(100))


        
