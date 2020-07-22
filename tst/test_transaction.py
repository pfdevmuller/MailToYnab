from datetime import datetime
from unittest import TestCase

from transaction import Transaction


class TestTransaction(TestCase):

    def test_ynab_dates(self):
        t = Transaction(datetime(2020, 11, 30), "vendor 1", 1234, "some_account")
        self.assertEqual("2020-11-30", t.ynab_date())
        self.assertEqual("2020-12-01", t.ynab_date_plus_days(1))
