from datetime import datetime
from unittest import TestCase

from account_matcher import CardSuffixAccountMatcher
from discovery_bank_za_parser import DiscoveryBankZaParser
from transaction import Transaction


class TestDiscoveryBankZaParser(TestCase):

    def test_get_transaction_no_match(self):
        text = b"Discovery Bank: R5.00 reserved on NO MATCH card ***1234 at Vendor Name. 01 Dec 09:21. Available balance: " \
               b"R1234.56. For more info, call 0860112265. "

        parser = DiscoveryBankZaParser("account123", CardSuffixAccountMatcher("1234"))
        transaction = parser.get_transaction(text, None)
        self.assertIsNone(transaction, "Expected null in response to non matching text.")


    def test_get_transaction(self):

        text = b"Card Payment\r\n\r\nVendor Name - R 3 401.90\r\n\r\nFrom Credit Card\r\n\r\n" \
               b"Card Ending ***1234\r\n\r\nSaturday 21 August at 11:32\r\n\r\nAvailable balance : R 12 345.67\r\n"

        parser = DiscoveryBankZaParser("account123", CardSuffixAccountMatcher("1234"))
        transaction = parser.get_transaction(text, "2021/08/21")

        expectation = Transaction(datetime(2021, 8, 21, 11, 32),
                                  "Vendor Name",
                                  -3401900,
                                  "account123")

        self.assertIsNotNone(transaction, "Expected transaction in response to matching text.")
        self.assertEqual(expectation.date, transaction.date, "Transaction dates should match.")
        self.assertEqual(expectation, transaction)
