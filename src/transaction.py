from datetime import timedelta


class Transaction:

    def __init__(self, date, vendor, amount, account):
        """
        amount should be int representing the currency milliunits
        (eg 1230 = R1.23 )
        vendor should be a String
        date should be a timezoned datetime
        """
        self.date = date
        self.vendor = vendor
        self.amount = amount
        self.account = account

    def ynab_date(self):
        return self.date.strftime("%Y-%m-%d")

    def ynab_date_plus_days(self, days):
        return (self.date + timedelta(days=days)).strftime("%Y-%m-%d")

    def __eq__(self, other):
        return self.date == other.date and self.vendor == other.vendor and \
               self.amount == other.amount and self.account == other.account

    def __str__(self):
        return (f"Transaction: date: {self.ynab_date()}, vendor: {self.vendor}"
                f", amount: {self.amount}, account: {self.account}")
