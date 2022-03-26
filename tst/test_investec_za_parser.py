from unittest import TestCase
from datetime import datetime

from account_matcher import CardSuffixAccountMatcher
from investec_za_parser import InvestecZaParser
from transaction import Transaction


class TestInvestecZaParser(TestCase):

    def test_get_transaction_no_match(self):
        text = b"A purchase has been authorised on your NO MATCH card ending 1234 for\r\nZAR5.00 at MTC CENTRE on 21/06/2019.  " \
               b"Your available balance is\r\nR6,809.39. "

        parser = InvestecZaParser("account123", CardSuffixAccountMatcher("1234"))
        transaction = parser.get_transaction(str(text, 'utf-8'), None)
        self.assertIsNone(transaction, "Expected null in response to non matching text.")

    def test_get_transaction(self):
        text = b"A purchase has been authorised on your Investec card ending 1234 for\r\nZAR5.00 at MTC CENTRE on 21/06/2019.  " \
               b"Your available balance is\r\nR6,809.39. "

        parser = InvestecZaParser("account123", CardSuffixAccountMatcher("1234"))
        transaction = parser.get_transaction(str(text, 'utf-8'), None)

        expectation = Transaction(datetime(2019, 6, 21),
                                  "MTC CENTRE",
                                  -5000,
                                  "account123")

        self.assertIsNotNone(transaction, "Expected transaction in response to matching text.")
        self.assertEqual(expectation, transaction)

    def test_regex_bug_2020_07_21(self):
        text = b"A purchase has been authorised on your Investec card ending 1234 for ZAR1,234.56 at PnP Crp Gardens on " \
               b"01/06/2020.  Your available balance is R12,345.67."

        parser = InvestecZaParser("account123", CardSuffixAccountMatcher("1234"))
        transaction = parser.get_transaction(str(text, 'utf-8'), None)

        expectation = Transaction(datetime(2020, 6, 1),
                                  "PnP Crp Gardens",
                                  -1234560,
                                  "account123")

        self.assertIsNotNone(transaction, "Expected transaction in response to matching text.")
        self.assertEqual(expectation, transaction)
