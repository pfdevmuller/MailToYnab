from unittest import TestCase

from investec_za_parser import InvestecZaParser


class TestInvestecZaParser(TestCase):
    def test_get_transaction(self):
        text = b"A purchase has been authorised on your Investec card ending 1234 for\r\nZAR5.00 at MTC CENTRE on 21/06/2019. " \
               b"Your available balance is\r\nR6,809.39. "

        parser = InvestecZaParser()
        self.assertTrue(parser.looks_like_notification(text), "Should recognise text as transaction.")
        groups = parser.extract_groups(text)
        self.assertIsNotNone(groups, "Should extract data from text")
        expectation = {
            "amount": "5.00",
            "amount_sign": -1,
            "account": "1234",
            "vendor": "MTC CENTRE",
            "date": "21/06/2019"}

        self.assertEquals(expectation, groups, "Expected specific data to be extracted")
