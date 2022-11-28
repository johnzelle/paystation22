# paystation.py

from datetime import datetime

class IllegalCoinException(Exception):
    pass


class PayStation:
    """Implements the 'business logic' of a parking pay  station.
    """

    LEGAL_COINS = [5, 10, 25]

    def __init__(self, factory):
        self._calculate_time = factory.create_rate_strategy()
        self._factory = factory
        self._reset()

    def add_payment(self, coinvalue):
        """Adds coinvalue in payment to the pay station

        pre: coinvalue is an int representing a legal coin
        note: raises IllegalCoinException if coinvalue invalid
        """
        if coinvalue not in self.LEGAL_COINS:
            raise IllegalCoinException(f"Bad coin: {coinvalue}")
        self._coins_inserted += coinvalue

    def read_display(self):
        """returns current number of minutes purchased"""
        return self._time_bought()

    def buy(self):
        """Terminates transaction and returns Receipt"""

        receipt = self._factory.create_receipt(self._time_bought())
        self._reset()
        return receipt

    def cancel(self):
        """Terminates the transaction (resets machine)"""

        self._reset()

    def _time_bought(self):
        return self._calculate_time(self._coins_inserted)

    def _reset(self):
        self._coins_inserted = 0


class Receipt:
    template = \
"""--------------------------------------------------
-------  P A R K I N G   R E C E I P T     -------
                Value {:03d} minutes.
              Car parked at {:02d}:{:02d}
--------------------------------------------------"""

    def __init__(self, value, barcode=False):
        self.value = value
        self.with_barcode = barcode

    def print(self, stream):
        now = datetime.now()
        output = self.template.format(self.value, now.hour, now.minute)
        print(output, file=stream)
        if self.with_barcode:
            print("||  | || | || ||| | ||| ||| | || ||", file=stream)
        


# rate strategies

class LinearRateStrategy:

    def __init__(self, cents_per_hour):
        self._center_per_hour = cents_per_hour

    def __call__(self, amount):
        return amount / self._center_per_hour * 60


# for backwards compatibility linear_rate_strategy is $1.50 an hour
# (5 cents buys 2 minutes)

linear_rate_strategy = LinearRateStrategy(150)


def progressive_rate_strategy(amount):
    if amount > 350:
        return 120 + (amount-350) // 5
    if amount > 150:
        return 60 + (amount-150) // 5 * 1.5
    return amount // 5 * 2


def is_weekend():
    today = datetime.now()
    return today.weekday() > 4


class AlternatingRateStrategy:

    def __init__(self, dec_strategy, weekend_rate, weekday_rate):
        self._is_weekend = dec_strategy
        self._weekend_rate_strat = weekend_rate
        self._weekday_rate_strat = weekday_rate

    def __call__(self, amount):
        if self._is_weekend():
            return self._weekend_rate_strat(amount)
        else:
            return self._weekday_rate_strat(amount)


# Abstract Factories for PayStation variants
class AlphaTownFactory:

    def create_rate_strategy(self):
        return LinearRateStrategy(150)

    def create_receipt(self, amt):
        return Receipt(amt)


class BetaTownFactory:

    def create_rate_strategy(self):
        return progressive_rate_strategy

    def create_receipt(self, amt):
        return Receipt(amt, barcode=True)


class TripoliFactory:

    def create_rate_strategy(self):
        return LinearRateStrategy(200)

    def create_receipt(self, amt):
        return Receipt(amt)

    
class GammaTownFactory:

    def create_rate_strategy(self):
        ars = AlternatingRateStrategy(is_weekend,
                                      progressive_rate_strategy,
                                      LinearRateStrategy(150))
        return ars

    def create_receipt(self, amt):
        return Receipt(amt)
