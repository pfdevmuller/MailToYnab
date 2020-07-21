from unittest import TestCase
from datetime import datetime

from investec_za_parser import InvestecZaParser
from transaction import Transaction


class TestInvestecZaParser(TestCase):

    def test_get_transaction_no_match(self):
        text = b"A purchase has been authorised on your NO MATCH card ending 1234 for\r\nZAR5.00 at MTC CENTRE on 21/06/2019.  " \
               b"Your available balance is\r\nR6,809.39. "

        parser = InvestecZaParser("account123")
        transaction = parser.get_transaction(text, None)
        self.assertIsNone(transaction, "Expected null in response to non matching text.")

    def test_get_transaction(self):
        text = b"A purchase has been authorised on your Investec card ending 1234 for\r\nZAR5.00 at MTC CENTRE on 21/06/2019.  " \
               b"Your available balance is\r\nR6,809.39. "

        parser = InvestecZaParser("account123")
        parser = InvestecZaParser("account123")
        transaction = parser.get_transaction(text, None)

        expectation = Transaction(datetime(2019, 6, 21),
                                  "MTC CENTRE",
                                  -5000,
                                  "account123")

        self.assertEqual(expectation, transaction)

