from unittest import TestCase
from datetime import datetime

from account_matcher import CardSuffixAccountMatcher
from investec_za_parser import InvestecZaParser
from transaction import Transaction


class TestInvestecZaParser(TestCase):


    def test_get_transaction_update(self):
        text = b"A purchase has been authorised on your Investec card ending 1234 for ZAR 1234.56 at SnapScan THE FIX Beans on 01 April 2023. Your available balance is R1.01."

        parser = InvestecZaParser("account123", CardSuffixAccountMatcher("1234"))
        transaction = parser.get_transaction(str(text, 'utf-8'), None)

        expectation = Transaction(datetime(2023, 4, 1),
                                  "SnapScan THE FIX Beans",
                                  -1234560,
                                  "account123")

        self.assertIsNotNone(transaction, "Expected transaction in response to matching text.")
        self.assertEqual(expectation, transaction)


    def test_get_transaction_no_match(self):
        text = b"A purchase has been authorised on your NO MATCH card ending 1234 for ZAR 1234.56 at SnapScan THE FIX Beans on 01 April 2023. Your available balance is R1.01."

        parser = InvestecZaParser("account123", CardSuffixAccountMatcher("1234"))
        transaction = parser.get_transaction(str(text, 'utf-8'), None)

        expectation = Transaction(datetime(2023, 4, 1),
                                  "SnapScan THE FIX Beans",
                                  -1234560,
                                  "account123")

        self.assertIsNone(transaction)
