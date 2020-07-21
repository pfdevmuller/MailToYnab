from unittest import TestCase

from config_provider import ConfigProvider, PARSER_PREFIX, ACCOUNT_MATCHER_PREFIX, ACCOUNT_PREFIX
from discovery_bank_za_parser import DiscoveryBankZaParser
from investec_za_parser import InvestecZaParser


class TestConfigProvider(TestCase):
    def test_get_parsers_none(self):
        keys = {'foo': 'bar'}

        config = ConfigProvider(keys)
        with self.assertRaises(Exception) as context:
            config.get_parsers()
        self.assertTrue("No parsers specified in config" in str(context.exception))

    def test_partially_specified_parser(self):
        keys = {PARSER_PREFIX + "_1": 'bar'}

        config = ConfigProvider(keys)
        with self.assertRaises(Exception) as context:
            config.get_parsers()
        self.assertTrue("Partially specified parser" in str(context.exception))

    def test_unknown_parser(self):
        keys = {PARSER_PREFIX + "_1": 'bar',
                ACCOUNT_PREFIX + "_1": 'bar',
                ACCOUNT_MATCHER_PREFIX + "_1": 'bar'}

        config = ConfigProvider(keys)
        with self.assertRaises(Exception) as context:
            config.get_parsers()
        self.assertTrue("Unknown parser requested" in str(context.exception))

    def test_get_parsers_two(self):
        keys = {PARSER_PREFIX + "_1": 'DiscoveryBankZaParser',
                ACCOUNT_PREFIX + "_1": 'account_disc',
                ACCOUNT_MATCHER_PREFIX + "_1": '1234',
                PARSER_PREFIX + "_2": 'InvestecZaParser',
                ACCOUNT_PREFIX + "_2": 'account_inv',
                ACCOUNT_MATCHER_PREFIX + "_2": '5678'}

        config = ConfigProvider(keys)
        parsers = config.get_parsers()

        self.assertEqual(2, len(parsers), "Expected two parsers")
        p1 = parsers[0]
        self.assertTrue(isinstance(p1, DiscoveryBankZaParser))
        self.assertEqual(p1.account, "account_disc")
        self.assertTrue(p1.account_matcher.matches("1234"))
        p2 = parsers[1]
        self.assertTrue(isinstance(p2, InvestecZaParser))
        self.assertEqual(p2.account, "account_inv")
        self.assertTrue(p2.account_matcher.matches("5678"))


