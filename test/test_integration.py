# test_integration.py

import unittest

from paystation.domain import PayStation, linear_rate_strategy


class TestAlphaTownIntegration(unittest.TestCase):

    def test_paystation_linear_rate(self):
        ps = PayStation(linear_rate_strategy)
        ps.add_payment(25)
        self.assertEqual(25 // 5 * 2, ps.read_display())
