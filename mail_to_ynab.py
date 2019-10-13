import os
from ynab_client import YnabClient
from mail_check import MailChecker
from discovery_za_parser import DiscoveryZaParser

class MailToYnab:

    def __init__(self, config_path):
        self.config = self.get_config(config_path)
        print(f"Config: {self.config}")

        api_key = self.config['ynab_api_key']
        budget_id = self.config['ynab_budget']
        account_id = self.config['ynab_account']
        self.ynab = YnabClient(api_key, budget_id, account_id)

        server = self.config['server']
        port = self.config['port']
        username = self.config['username']
        password = self.config['password']
        self.mail = MailChecker(server, port, username, password)

        self.parser = DiscoveryZaParser()

    def run(self):
        for msg in self.mail.list_inbox():
            text = self.mail.extract_text(msg)
            if self.parser.looks_like_notification(text):
                print("Looks like a notification")
                transaction = self.parser.get_transaction(text)
                isKnown = self.ynab.isExisting(transaction)
                if (isKnown):
                    print("This transaction is known")
                else:
                    print("This transaction is new!")
            else:
                print("Not what we are looking for")

    def get_config(self, path):
        config = {}
        f= open(path,'r')
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
    config_path = home +'/.mail_to_ynab'
    mty = MailToYnab(config_path)
    mty.run()
