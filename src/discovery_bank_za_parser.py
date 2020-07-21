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

    def __init__(self, account):
        self.account = account

    def get_transaction(self, text, message_date):
        fields = self.extract_groups(text)
        if fields:
            amount = (int(round(float(fields["amount"]) * 1000))
                      * fields["amount_sign"])
            vendor = fields["vendor"]
            year = dateparser.parse(message_date).year
            date_str = str(year) + " " + fields["date"]
            date = datetime.strptime(date_str, "%Y %d %b %H:%M")
            print(f"Fields extracted from mail: {fields}")
            t = Transaction(date, vendor, amount, self.account)
            print(f"Transaction is: {t}")
            return t
        else:
            return None

    def extract_groups(self, text):
        # Sample:
        # b'Discovery Bank: R5.00 reserved on card ***1234 at Vendor Name. 01 Dec 09:21. Available balance: R1234.56. For more info, call 0860112265.<!doctype html>\n<html>\n    <head><meta charset="UTF-8">\n        <title>Disclaimer</title>\n    </head>\n    <body>\n        <table align="center" bgcolor="#ffffff" cellpadding="0" cellspacing="0" width="600">\n                <tr>\n                    <td align="left" style="font-family: calibri, Arial, sans-serif; color: #292b2c; font-size: 8px; padding-top: 10px; padding-bottom: 10px;">Discovery Bank Ltd. Registration no 2015/408745/06. An authorised financial services and registered credit provider. FSP no 48657. NCR registration no NCRCP9997. Limits, Ts &amp; Cs apply. See full disclaimer here.</td>\n                </tr>\n        </table>\n    </body>\n</html>\n' # noqa

        # This is the section you care about:
        # Discovery Bank: R5.00 reserved on card ***1234 at Vendor Name. 01 Dec 09:21. Available balance: R1234.56. For more info, call 0860112265. # noqa
        # TODO test this before modifying it for PEP8 compliance
        pattern_reserved = "Discovery Bank: R(\d+\.\d+) reserved on card.*?(\d+) at (.+?)\. (\d\d \w\w\w \d\d:\d\d)\. Available balance"  # noqa

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

        # TODO assumption about encoding
        text = str(text, 'utf-8').replace('\r\n', ' ')

        for pattern, sign in zip(patterns, amount_signs):
            result = re.search(pattern, text)
            if result:
                groups = {
                    "amount": result.groups()[0],
                    "amount_sign": sign,
                    # TODO: actually sometimes the last four digits of the
                    # card, not the account
                    "account": result.groups()[1],
                    "vendor": result.groups()[2],
                    "date": result.groups()[3]}
                return groups
        return None
