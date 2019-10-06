import re

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
        print(f"Best we have at the moment: {fields}")

    def extract_groups(self, text):
        # Sample:
        # b'---------- Forwarded message ---------\nFrom: <incontact@discoverycard.co.za>\nDate: Sat, 5 Oct 2019 at 09:35\nSubject: DiscoveryCard: R789.23 reserved for purchase @ The Vendor Name\nfrom card a/c..123456 using card..9876. 5Oct 09:35\nTo: <some_user@gmail.com>\n\n\nDiscoveryCard: R789.23 reserved for purchase @ The Vendor Name from card\na/c..123456 using card..9876. Avail R1234.  5Oct 09:35\n'
        # This is the section you care about:
        # DiscoveryCard: R789.23 reserved for purchase @ The Vendor Name from card\na/c..123456 using card..9876. Avail R1234.  5Oct 09:35\n
        pattern = "DiscoveryCard: R(\d+\.\d+) reserved for purchase @ (.+?) from card.*?(\d+) using card\.+\d+\. Avail R\d+\.\ +(\d+\w+ \d+:\d+)"
        # TODO assumption about encoding
        text = str(text, 'utf-8').replace('\n', ' ')
        result = re.search(pattern, text)
        if result:
            print(result.groups())
            return {
                "amount" : result.groups()[0],
                "vendor" : result.groups()[1],
                "account" : result.groups()[2],
                "date" : result.groups()[3]}
        else:
            return None
