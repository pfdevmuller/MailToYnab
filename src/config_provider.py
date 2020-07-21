# Config Keys
from account_matcher import CardSuffixAccountMatcher
from discovery_bank_za_parser import DiscoveryBankZaParser
from investec_za_parser import InvestecZaParser

USERNAME = "username"
PASSWORD = "password"
SERVER = "server"
PORT = "port"
API_KEY = "ynab_api_key"
BUDGET = "ynab_budget"

PARSER_PREFIX = "parser"
ACCOUNT_PREFIX = "ynab_account"
ACCOUNT_MATCHER_PREFIX = "matcher"


class ConfigProvider(object):

    def __init__(self, config_pairs):
        self.config = config_pairs

    def api_key(self):
        return self.config[API_KEY]

    def budget_id(self):
        return self.config[BUDGET]

    def server(self):
        return self.config[SERVER]

    def port(self):
        return self.config[PORT]

    def username(self):
        return self.config[USERNAME]

    def password(self):
        return self.config[PASSWORD]

    def get_parsers(self):
        parsers = []
        index = 1
        while True:
            parser = self.get_parser(index)
            if parser:
                parsers.append(parser)
                index += 1
            else:
                break
        if len(parsers) == 0:
            raise Exception("No parsers specified in config.")
        else:
            return parsers

    def get_parser(self, parser_index):
        parser_key = PARSER_PREFIX + "_" + str(parser_index)
        account_key = ACCOUNT_PREFIX + "_" + str(parser_index)
        matcher_key = ACCOUNT_MATCHER_PREFIX + "_" + str(parser_index)
        parser_name = self.config.get(parser_key)
        account = self.config.get(account_key)
        account_matcher_str = self.config.get(matcher_key)

        if parser_name and account and account_matcher_str:
            if parser_name == "DiscoveryBankZaParser":
                print(
                    f"Creating DiscoveryBankZaParser with CardSuffixAccountMatcher on {account_matcher_str} for account {account}")
                return DiscoveryBankZaParser(account, CardSuffixAccountMatcher(account_matcher_str))
            elif parser_name == "InvestecZaParser":
                print(
                    f"Creating InvestecZaParser with CardSuffixAccountMatcher on {account_matcher_str} for account {account}")
                return InvestecZaParser(account, CardSuffixAccountMatcher(account_matcher_str))
            else:
                raise Exception(f"Unknown parser requested: {[parser_name]}")
        elif parser_name or account or account_matcher_str:
            raise Exception(
                f"Partially specified parser: {parser_key}={parser_name}, {account_key}={account}, {matcher_key}={account_matcher_str}")
        else:
            return None
