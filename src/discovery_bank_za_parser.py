import re
from dateutil import parser as dateparser
from datetime import datetime
from transaction import Transaction


# Notification parser for Transaction Update notifications from the
# Discovery Bank in South Africa, which is replacing the Discovery Credit
# Card Provider
# These are distinct from the InContact notifications provided by the
# Discovery Credit Card provider
class DiscoveryBankZaParser:

    def __init__(self, account, account_matcher):
        self.account = account
        self.account_matcher = account_matcher

    def get_transaction(self, text, message_date):
        fields = self.extract_groups(text)
        if fields:
            if self.account_matcher.matches(fields["card_suffix"]):
                amount_str = fields["amount"].replace(' ', '')
                amount = (int(round(float(amount_str) * 1000))
                          * fields["amount_sign"])
                vendor = fields["vendor"]
                year = dateparser.parse(message_date).year
                date_str = "%s %s" % (str(year), fields["date"])
                date = datetime.strptime(date_str, "%Y %d %B at %H:%M")
                print(f"Fields extracted from mail: {fields}")
                t = Transaction(date, vendor, amount, self.account)
                print(f"Transaction is: {t}")
                return t

        return None

    @staticmethod
    def extract_groups(text):
        text = text.replace('\r\n', ' ').replace('\n', ' ')
        text = text.replace(u"–", '-')  # replace em dash

        pattern_reserved = r"Card payment (.+?) - R\xa0([\d ]+\.\d\d) " \
                           r"From Credit Card Card ending \*\*\*(\d+) " \
                           r"\w+, (\d+ \w+ at \d\d:\d\d)"

        # The phrase "reserved on card" can also be:
        #
        # "reversed on card" -> implies inversion of amount
        # Example:
        # Discovery Bank: R8.00 reversed on card ***1234 at GOOGLE *TEMPORARY HOLD 05\nDec 20:28. Available balance: R1234.56. For more info, call 0860112265. # noqa
        # TODO test this before modifying it for PEP8 compliance
        pattern_reversed = "Discovery Bank: R(\d+\.\d+) reversed on card.*?(\d+) at (.+?) (\d\d \w\w\w \d\d:\d\d)\. Available balance"  # noqa

        # Or:
        # "paid to account" -> implies inversion of amount
        # Example:
        # Discovery Bank: R96.94 paid to account ***1234. Ref: "Some Vendor". 08 Dec 15:39. Available balance: R1234.56. For more info,\ncall 0860112265. # noqa
        # TODO test this before modifying it for PEP8 compliance
        pattern_paid = "Discovery Bank: R(\d+\.\d+) paid to account.*?(\d+). Ref: \"(.+?)\". (\d\d \w\w\w \d\d:\d\d)\. Available balance"  # noqa

        patterns = [pattern_reserved, pattern_reversed, pattern_paid]
        amount_signs = [-1, 1, 1]

        for pattern, sign in zip(patterns, amount_signs):
            result = re.search(pattern, text, re.M)
            if result:
                groups = {
                    "vendor": result.groups()[0],
                    "amount": result.groups()[1],
                    "amount_sign": sign,
                    "card_suffix": result.groups()[2],
                    "date": result.groups()[3]}
                return groups
        return None
