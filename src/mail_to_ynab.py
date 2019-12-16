import sys
import os
from ynab_client import YnabClient
from mail_check import InboxScan
from mail_check import MailChecker
from discovery_bank_za_parser import DiscoveryBankZaParser

class MailToYnab:

    def __init__(self, config_path, dryrun = False):
        self.dryrun = dryrun
        if self.dryrun:
            print("DRYRUN: No changes to YNAB or email will be made.")
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

        self.parser = DiscoveryBankZaParser()

    def run(self):
        upload_count = 0
        delete_count = 0
        unparsed_count = 0
        inbox_scan = self.mail.start_inbox_scan()
        for msg in inbox_scan.messages():
            text = self.mail.extract_text(msg)
            if self.parser.looks_like_notification(text):
                print("Looks like a notification")
                msg_date = msg["Date"]
                transaction = self.parser.get_transaction(text, msg_date)
                isKnown = self.ynab.isExisting(transaction)
                if (isKnown):
                    print("This transaction is known")
                    if self.dryrun:
                        print("DRYRUN: no email delete")
                    else:
                        inbox_scan.delete_current()
                        delete_count += 1
                else:
                    print("This transaction is new!")
                    if self.dryrun:
                        print("DRYRUN: no transaction upload")
                    else:
                        self.ynab.uploadTransaction(transaction)
                        upload_count += 1
            else:
                print("Not what we are looking for")
                unparsed_count += 1
        inbox_scan.close() # This commits any deletes we marked above
        print(f"Uploaded {upload_count} transactions. Deleted {delete_count} emails. Left {unparsed_count} emails unparsed because they did not match the parser.")

    def test_ynab(self):
        print("Testing ynab")
        self.ynab.test_connection()

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
    dryrun = "dryrun" in sys.argv
    mty = MailToYnab(config_path, dryrun)
    print(f"sys.argv: {sys.argv}")
    if ("test-ynab" in sys.argv):
        mty.test_ynab()
    else:
        mty.run()

def lambda_handler(event, context):
    print("This is actual Mail To Ynab")
    return {'message' : 'completed - mail to ynab'}

# import code; code.interact(local=dict(globals(), **locals()))

