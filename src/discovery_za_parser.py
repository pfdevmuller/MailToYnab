import re
from dateutil import parser as dateparser
from datetime import datetime
from transaction import Transaction


# Notification parser for InContact notification from the Discovery credit
# card provider in South Africa
class DiscoveryZaParser:

    def __init__(self, account):
        self.account = account

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
        year = dateparser.parse(message_date).year
        date_str = str(year) + " " + fields["date"]
        date = datetime.strptime(date_str, "%Y %d%b %H:%M")
        print(f"Fields extracted from mail: {fields}")
        t = Transaction(date, vendor, -amount, self.account)
        print(f"Transaction is: {t}")
        return t

    def extract_groups(self, text):
        # Sample:
        # b'---------- Forwarded message ---------\nFrom: <incontact@discoverycard.co.za>\nDate: Sat, 5 Oct 2019 at 09:35\nSubject: DiscoveryCard: R789.23 reserved for purchase @ The Vendor Name\nfrom card a/c..123456 using card..9876. 5Oct 09:35\nTo: <some_user@gmail.com>\n\n\nDiscoveryCard: R789.23 reserved for purchase @ The Vendor Name from card\na/c..123456 using card..9876. Avail R1234.  5Oct 09:35\n' # noqa
        # This is the section you care about:
        # DiscoveryCard: R789.23 reserved for purchase @ The Vendor Name from card\na/c..123456 using card..9876. Avail R1234.  5Oct 09:35\n # noqa
        # TODO write a test for this before you try to make it pep8 compliant
        pattern = "DiscoveryCard: R(\d+\.\d+) reserved for purchase @ (.+?) from card.*?(\d+) using card\.+\d+\. Avail R\d+\.\ +(\d+\w+ \d+:\d+)"  # noqa

        # TODO assumption about encoding
        text = str(text, 'utf-8').replace('\n', ' ')
        result = re.search(pattern, text)
        if result:
            return {
                "amount": result.groups()[0],
                "vendor": result.groups()[1],
                "account": result.groups()[2],
                "date": result.groups()[3]}
        else:
            return None
