# test_integration.py

import unittest


from paystation.domain import (PayStation,
                               linear_rate_strategy,
                               LinearRateStrategy,
                               progressive_rate_strategy,
                               AlternatingRateStrategy,
                               is_weekend
                               )


def insert_coins(ps, coins):
    for coin in coins:
        ps.add_payment(coin)


class TestAlphaTownIntegration(unittest.TestCase):

    def test_paystation_linear_rate(self):
        ps = PayStation(linear_rate_strategy)
        ps.add_payment(25)
        self.assertEqual(25//5*2, ps.read_display())

    def test_paystation_new_linear_rate(self):
        rate = LinearRateStrategy(200)
        ps = PayStation(rate)
        ps.add_payment(25)
        self.assertEqual(rate(25), ps.read_display())
        


class TestBetaTownIntegration(unittest.TestCase):

    def test_paystation_progressive_rate(self):
        ps = PayStation(progressive_rate_strategy)
        insert_coins(ps, [25, 25, 25, 25, 25, 25])
        self.assertEqual(150//5*2, ps.read_display())
        insert_coins(ps, [25, 25, 25, 25, 25, 25, 25, 25])
        self.assertEqual(150//5*2+200//5*1.5, ps.read_display())
        insert_coins(ps, [25])
        self.assertEqual(150//5*2 + 200//5*1.5 + 25//5, ps.read_display())


class TestGammaTownIntegration(unittest.TestCase):

    def _insert_coins(self, ps, coins):
        for coin in coins:
            ps.add_payment(coin)

    def test_paystion_alternating_rate(self):
        ars = AlternatingRateStrategy(is_weekend,
                                      progressive_rate_strategy,
                                      linear_rate_strategy)
        ps = PayStation(ars)
        insert_coins(ps, [25]*12)
        if is_weekend():
            self.assertEqual(progressive_rate_strategy(25*12),
                             ps.read_display())
        else:
            self.assertEqual(linear_rate_strategy(25*12),
                             ps.read_display())
