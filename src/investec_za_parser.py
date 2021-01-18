import re
from datetime import datetime
from transaction import Transaction


# Notification parser for Purchase Notifications from the
# Investec Bank in South Africa
class InvestecZaParser(object):

    def __init__(self, account, account_matcher):
        self.account = account
        self.account_matcher = account_matcher

    def get_transaction(self, text, message_date):
        fields = self.extract_groups(text)
        if fields:
            if self.account_matcher.matches(fields["card_suffix"]):
                amount_str = fields["amount"]
                amount_str = amount_str.replace(',', '')
                amount = (int(round(float(amount_str) * 1000))
                          * fields["amount_sign"])
                vendor = fields["vendor"]
                date = datetime.strptime(fields["date"], "%d/%m/%Y")
                print(f"Fields extracted from mail: {fields}")
                t = Transaction(date, vendor, amount, self.account)
                print(f"Transaction is: {t}")
                return t

        return None

    def extract_groups(self, text):
        # Sample:
        # b"A purchase has been authorised on your Investec card ending 1234 for\r\nZAR5.00 at MTC CENTRE on 21/06/2019. Your available balance is\r\nR6,809.39." # noqa
        pattern_authorised = r'A purchase has been authorised on your Investec card ending (\d+) for.*?(ZAR|NAD)([\d\.,]+) at (.+?) on ' \
                             r'(\d\d/\d\d/\d\d\d\d). +Your available balance '

        patterns = [pattern_authorised]
        amount_signs = [-1]

        # TODO assumption about encoding
        text = str(text, 'utf-8').replace('\r\n', ' ')

        for pattern, sign in zip(patterns, amount_signs):
            result = re.search(pattern, text)
            if result:
                groups = {
                    "amount": result.groups()[2],
                    "amount_sign": sign,
                    "card_suffix": result.groups()[0],
                    "vendor": result.groups()[3],
                    "date": result.groups()[4]}
                return groups
        return None
