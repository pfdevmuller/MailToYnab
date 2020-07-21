import re
from datetime import datetime
from transaction import Transaction


# Notification parser for Purchase Notifications from the
# Investec Bank in South Africa
class InvestecZaParser:

    def looks_like_notification(self, text):
        if self.extract_groups(text):
            # TODO check if the account is as expected
            return True
        else:
            return False

    def get_transaction(self, text, message_date):
        fields = self.extract_groups(text)
        amount = (int(round(float(fields["amount"]) * 1000))
                  * fields["amount_sign"])
        vendor = fields["vendor"]
        date = datetime.strptime(fields["date"], "%d/%m/%Y")
        print(f"Fields extracted from mail: {fields}")
        t = Transaction(date, vendor, amount)
        print(f"Transaction is: {t}")
        return t

    def extract_groups(self, text):
        # Sample:
        # b"A purchase has been authorised on your Investec card ending 1234 for\r\nZAR5.00 at MTC CENTRE on 21/06/2019. Your available balance is\r\nR6,809.39." # noqa
        pattern_authorised = r'A purchase has been authorised on your Investec card ending (\d+) for.*?ZAR(\d+\.\d+) at (.+?) on ' \
                             r'(\d\d/\d\d/\d\d\d\d). Your available balance '

        patterns = [pattern_authorised]
        amount_signs = [-1]

        # TODO assumption about encoding
        text = str(text, 'utf-8').replace('\r\n', ' ')

        for pattern, sign in zip(patterns, amount_signs):
            result = re.search(pattern, text)
            if result:
                groups = {
                    "amount": result.groups()[1],
                    "amount_sign": sign,
                    # TODO: actually sometimes the last four digits of the
                    # card, not the account
                    "account": result.groups()[0],
                    "vendor": result.groups()[2],
                    "date": result.groups()[3]}
                return groups
        return None
