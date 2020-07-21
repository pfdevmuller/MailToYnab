import swagger_client as ynab
from swagger_client.rest import ApiException


class YnabClient:

    def __init__(self, api_key, budget_id):
        self.key = api_key
        self.budget = budget_id
        configuration = ynab.Configuration()
        configuration.api_key['Authorization'] = self.key
        configuration.api_key_prefix['Authorization'] = 'Bearer'

    def upload_transaction(self, transaction):
        wrapper = ynab.SaveTransactionsWrapper()
        wrapper.transaction = ynab.SaveTransaction(
            account_id=transaction.account,
            _date=transaction.ynab_date(),
            amount=transaction.amount,
            payee_name=transaction.vendor)
        print(f"Uploading: {wrapper}")
        ynab.TransactionsApi().create_transaction(wrapper, self.budget)

    # TODO this seems well worth testing
    def is_existing(self, transaction):
        try:
            since_date = transaction.ynab_date()
            resp = ynab.TransactionsApi().get_transactions_by_account(
                self.budget, transaction.account, since_date=since_date)
            transactions = resp.data["transactions"]
            for t in transactions:
                match = self.looks_like(transaction, t)
                if match:
                    return True
        except ApiException as e:
            print("Exception %s\n" % e)
            raise e

    @staticmethod
    def looks_like(transaction, ynab_transaction):
        t = transaction
        yt = ynab_transaction
        # print(f"Comparing {t} with {yt}")
        # Vendor names from statement are more complete than from
        # notifications, so we need to be a little lenient
        is_vendor_samey = ((t.vendor.lower() in yt["payee_name"].lower()) or
                           (yt["payee_name"].lower() in t.vendor.lower()))
        is_date_same = t.ynab_date() == yt["date"]
        is_amount_same = t.amount == yt["amount"]
        return is_date_same and is_amount_same and is_vendor_samey

    @staticmethod
    def test_connection():
        budgets = ynab.BudgetsApi().get_budgets()
        print(f"Call made, result is: {budgets}")

# import code; code.interact(local=dict(globals(), **locals()))
