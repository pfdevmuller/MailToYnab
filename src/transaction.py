class Transaction:

    def __init__(self, date, vendor, amount):
        """
        amount should be int representing the currency milliunits
        (eg 1230 = R1.23 )
        vendor should be a String
        date should be a timezoned datetime
        """
        self.date = date
        self.vendor = vendor
        self.amount = amount

    def ynab_date(self):
        return self.date.strftime("%Y-%m-%d")

    def __str__(self):
        return (f"Transaction: date: {self.ynab_date()}, vendor: {self.vendor}"
                f", amount: {self.amount}")
