import re
from dateutil import parser as DateParser
from datetime import datetime
from transaction import Transaction

# Notification parser for Transaction Update notification from the Discovery Bank in South Africa,
# which is replacing the Discovery Credit Card Provider
# Distinct from the InContact notifications provided by the Discovery Credit Card provider
class DiscoveryBankZaParser:

    def looks_like_notification(self, text):
        if self.extract_groups(text):
            # TODO check if the account is as expected
            return True
        else:
            return False

    def get_transaction(self, text, message_date):
        fields = self.extract_groups(text)
        amount = int(round(float(fields["amount"]) * 1000))
        vendor = fields["vendor"]
        year = DateParser.parse(message_date).year
        date_str = str(year) + " " + fields["date"]
        date = datetime.strptime(date_str, "%Y %d %b %H:%M")
        print(f"Fields extracted from mail: {fields}")
        t = Transaction(date, vendor, -amount)
        print(f"Transaction is: {t}")
        return t

    def extract_groups(self, text):
        # Sample:
        # b'Discovery Bank: R5.00 reserved on card ***1234 at Vendor Name. 01 Dec 09:21. Available balance: R1234.56. For more info, call 0860112265.<!doctype html>\n<html>\n    <head><meta charset="UTF-8">\n        <title>Disclaimer</title>\n    </head>\n    <body>\n        <table align="center" bgcolor="#ffffff" cellpadding="0" cellspacing="0" width="600">\n                <tr>\n                    <td align="left" style="font-family: calibri, Arial, sans-serif; color: #292b2c; font-size: 8px; padding-top: 10px; padding-bottom: 10px;">Discovery Bank Ltd. Registration no 2015/408745/06. An authorised financial services and registered credit provider. FSP no 48657. NCR registration no NCRCP9997. Limits, Ts &amp; Cs apply. See full disclaimer here.</td>\n                </tr>\n        </table>\n    </body>\n</html>\n'
        # This is the section you care about:
        # Discovery Bank: R5.00 reserved on card ***1234 at Vendor Name. 01 Dec 09:21. Available balance: R1234.56. For more info, call 0860112265.
        pattern = "Discovery Bank: R(\d+\.\d+) reserved on card.*?(\d+) at (.+?)\. (\d\d \w\w\w \d\d:\d\d)\. Available balance"

        # TODO assumption about encoding
        text = str(text, 'utf-8').replace('\n', ' ')
        result = re.search(pattern, text)
        if result:
            groups = {
                "amount" : result.groups()[0],
                "account" : result.groups()[1], # TODO: actually the last four digits of the card, not the account
                "vendor" : result.groups()[2],
                "date" : result.groups()[3]}
            return groups
        else:
            return None
