import re
from datetime import datetime
from transaction import Transaction

# Notification parser for InContact notification from the Discovery credit card provider in South Africa
class DiscoveryZaParser:

    def looks_like_notification(self, text):
        if self.extract_groups(text):
            # TODO check if the account is as expected
            return True
        else:
            return False

    def get_transaction(self, text):
        fields = self.extract_groups(text)
        amount = int(round(float(fields["amount"]) * 1000))
        vendor = fields["vendor"]
        date_str = fields["year"] + " " + fields["date"]
        date = datetime.strptime(date_str, "%Y %d%b %H:%M")
        print(f"Fields extracted from mail: {fields}")
        t = Transaction(date, vendor, amount)
        print(f"Transaction is: {t}")
        return t

    def extract_groups(self, text):
        # Sample:
        # b'---------- Forwarded message ---------\nFrom: <incontact@discoverycard.co.za>\nDate: Sat, 5 Oct 2019 at 09:35\nSubject: DiscoveryCard: R789.23 reserved for purchase @ The Vendor Name\nfrom card a/c..123456 using card..9876. 5Oct 09:35\nTo: <some_user@gmail.com>\n\n\nDiscoveryCard: R789.23 reserved for purchase @ The Vendor Name from card\na/c..123456 using card..9876. Avail R1234.  5Oct 09:35\n'
        # This is the section you care about:
        # DiscoveryCard: R789.23 reserved for purchase @ The Vendor Name from card\na/c..123456 using card..9876. Avail R1234.  5Oct 09:35\n
        # However the date in that line does not have a year, so we pull that out of the date line.
        # TODO: This could be simplied, just use the date line for the date and ignore it on the body line.
        pattern = "Date: \w+, \d+ \w+ (\d{4}) at.+DiscoveryCard: R(\d+\.\d+) reserved for purchase @ (.+?) from card.*?(\d+) using card\.+\d+\. Avail R\d+\.\ +(\d+\w+ \d+:\d+)"

        # TODO assumption about encoding
        text = str(text, 'utf-8').replace('\n', ' ')
        result = re.search(pattern, text)
        if result:
            return {
                "year" : result.groups()[0],
                "amount" : result.groups()[1],
                "vendor" : result.groups()[2],
                "account" : result.groups()[3],
                "date" : result.groups()[4]}
        else:
            return None
