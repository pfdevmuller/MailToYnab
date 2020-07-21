import sys
import os
import json
from ynab_client import YnabClient
from mail_check import MailChecker
from discovery_bank_za_parser import DiscoveryBankZaParser
from investec_za_parser import InvestecZaParser


class MailToYnab:

    def __init__(self, cfg, dryrun=False):
        self.dryrun = dryrun
        if self.dryrun:
            print("DRYRUN: No changes to YNAB or email will be made.")
        self.config = cfg

        api_key = self.config['ynab_api_key']
        budget_id = self.config['ynab_budget']
        account_id = self.config['ynab_account']
        self.ynab = YnabClient(api_key, budget_id)

        server = self.config['server']
        port = self.config['port']
        username = self.config['username']
        password = self.config['password']
        self.mail = MailChecker(server, port, username, password)

        # First parser to successfully extract a notification will be used
        self.parsers = [DiscoveryBankZaParser(account_id), InvestecZaParser(account_id)]

    def run(self):
        upload_count = 0
        delete_count = 0
        unparsed_count = 0
        inbox_scan = self.mail.start_inbox_scan()
        for msg in inbox_scan.messages():
            parsed = False
            text = self.mail.extract_text(msg)
            for parser in self.parsers:
                if parsed:
                    # Only the first successful parser should be used
                    break
                transaction = parser.get_transaction(text, msg["Date"])
                if transaction:
                    parsed = True
                    print("Looks like a notification")
                    is_known = self.ynab.is_existing(transaction)
                    if is_known:
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
                            self.ynab.upload_transaction(transaction)
                            upload_count += 1
            if not parsed:
                print("Not what we are looking for")
                unparsed_count += 1
        inbox_scan.close()  # This commits any deletes we marked above
        msg = (f"Uploaded {upload_count} transactions. Deleted {delete_count}"
               f" emails. Left {unparsed_count} emails unparsed because they"
               f" did not match the parsers.")
        print(msg)
        return msg

    def test_ynab(self):
        print("Testing ynab")
        self.ynab.test_connection()


def get_config_from_file(path):
    cfg = {}
    f = open(path, 'r')
    lines = f.readlines()
    for line in lines:
        if line[0] == '#':
            continue
        tokens = line.split(':')
        if len(tokens) != 2:
            raise Exception("Expected config lines to contain exactly two fields")
        key = tokens[0].strip()
        value = tokens[1].strip()
        cfg[key] = value
    return cfg


def get_config_from_env():
    return os.environ


def local_handler():
    home = os.getenv("HOME")
    config_path = home + '/.mail_to_ynab'
    config = get_config_from_file(config_path)
    if "dump-config" in sys.argv:
        structure = {"Variables": config}
        print(json.dumps(structure))
        sys.exit()
    dryrun = "dryrun" in sys.argv
    mty = MailToYnab(config, dryrun)
    print(f"sys.argv: {sys.argv}")
    if "test-ynab" in sys.argv:
        mty.test_ynab()
    else:
        mty.run()


def lambda_handler(event, context):
    print("This is actual Mail To Ynab")
    config = get_config_from_env()
    dryrun = False
    mty = MailToYnab(config, dryrun)
    result = mty.run()
    return {'message': result}


if __name__ == "__main__":
    local_handler()

# import code; code.interact(local=dict(globals(), **locals()))
