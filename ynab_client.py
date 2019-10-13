import swagger_client as ynab
from swagger_client.rest import ApiException
from transaction import Transaction

class YnabClient:

    def __init__(self, api_key, budget_id, account_id):
        self.key = api_key
        self.budget = budget_id
        self.account = account_id
        configuration = ynab.Configuration()
        configuration.api_key['Authorization'] = self.key
        configuration.api_key_prefix['Authorization'] = 'Bearer'

    # TODO this seems well worth testing
    def isExisting(self, transaction):
        try:
            since_date = "2018-02-02"#transaction.ynab_date()
            resp = ynab.TransactionsApi().get_transactions_by_account(self.budget, self.account, since_date=since_date)
            transactions = resp.data["transactions"]
            for t in transactions:
                match = self.looks_like(transaction, t)
                print(f"Match? {match}")
        except ApiException as e:
            print("Exception %s\n" % e)
            raise e

    def looks_like(self, transaction, ynab_transaction):
        t = transaction
        yt = ynab_transaction
        print(f"Comparing {t} with {yt}")
        # TODO fetch payee using payee id and match it to vendor
        return (t.date == yt["date"] and
                t.amount == yt["amount"])

# import code; code.interact(local=dict(globals(), **locals()))
