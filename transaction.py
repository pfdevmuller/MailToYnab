class Transaction:

    def __init__(self, date, vendor, amount):
        """
        amount should be int representing the currency milliunits (eg 1230 = R1.23 )
        vendor should be a String
        date should be a timezoned datetime
        """
        self.date = date
        self.vendor = vendor
        self.amount = amount


    def __str__(self):
        pretty_date = self.date.strftime("%Y-%m-%d")
        return f"Transaction: date: {pretty_date}, vendor: {self.vendor}, amount: {self.amount}"
