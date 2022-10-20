# paystation.py

class IllegalCoinException(Exception):
    pass

class PayStation:
    """Implements the 'business logic' of a parking pay  station.
    """

    LEGAL_COINS = [5, 10, 25]

    def __init__(self):
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
        
        receipt = Receipt(self._time_bought())
        self._reset()
        return receipt
    
    def cancel(self):
        """Terminates the transaction (resets machine)"""

        self._reset()

    def _time_bought(self):
        return self._coins_inserted // 5 * 2

    def _reset(self):
        self._coins_inserted = 0
        

class Receipt:

    def __init__(self, value):
        self.value = value