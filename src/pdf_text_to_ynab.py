from datetime import datetime
import re
import os
from ynab_client import YnabClient
from transaction import Transaction


# This is not currently a proper implementation, it is a partially hardcoded
# once-off I needed to extract a single month from pdf. It can however be
# generalized with a bit of love. If this is done, a PdfParser should be
# broken out and specialized for different statement formats.
# The currently implementation also doesn't actually work against PDFs, it
# takes a text file I pre-generated with pdftotext and grep.
class PdfToYnab:

    def __init__(self, config_path):
        self.config = self.get_config(config_path)
        print(f"Config: {self.config}")

        api_key = self.config['ynab_api_key']
        budget_id = self.config['ynab_budget']
        account_id = self.config['ynab_account']
        self.ynab = YnabClient(api_key, budget_id, account_id)

    def run(self, infile):
        with open(infile, 'r') as f:
            for line in f:
                transaction = self.get_transaction(line)
                if transaction:
                    isKnown = self.ynab.is_existing(transaction)
                    if (isKnown):
                        print("This transaction is known")
                    else:
                        print("This transaction is new!")
                        self.ynab.upload_transaction(transaction)
                else:
                    print("Not what we are looking for")

    def get_transaction(self, line):
        print(f"line is: {line}")

        # TODO test this before you make it pep8 compliant
        pattern = " +(\d+) Nov +([\&\#\-\.\*\(\w\ ]+?)    \ +([\d\.\,]+)"  # noqa
        result = re.search(pattern, line)
        # TODO WARN HARDCODING HERE
        date_str = "2019-11-" + result.groups()[0]
        date = datetime.strptime(date_str, "%Y-%m-%d")
        amount = int(round(float(result.groups()[2].replace(",", "")) * 1000))
        if line.rstrip()[-2:] != "Cr":
            amount = -amount
        vendor = result.groups()[1].rstrip()
        t = Transaction(date, vendor, amount)
        print(f"Transaction is: {t}")
        return t

    def get_config(self, path):
        config = {}
        f = open(path, 'r')
        lines = f.readlines()
        for l in lines:
            tokens = l.split(':')
            if len(tokens) != 2:
                raise "Expected config lines to contain exactly two fields"
            key = tokens[0].strip()
            value = tokens[1].strip()
            config[key] = value
        return config


if __name__ == "__main__":
    home = os.getenv("HOME")
    config_path = home + '/.mail_to_ynab'
    mty = PdfToYnab(config_path)
    # TODO WARN HARDCODING HERE
    infile = '/Users/mullerp/Downloads/lines'
    mty.run(infile)

# import code; code.interact(local=dict(globals(), **locals()))
