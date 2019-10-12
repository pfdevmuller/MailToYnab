from __future__ import print_function
import time
import swagger_client as ynab
from swagger_client.rest import ApiException
from pprint import pprint

class YnabClient:

    def __init__(self, api_key, budget_id, account_id):
        self.key = api_key
        self.budget = budget_id
        self.account = account_id
        configuration = ynab.Configuration()
        configuration.api_key['Authorization'] = self.key
        configuration.api_key_prefix['Authorization'] = 'Bearer'

    def test_ynab(self):
        try:
            pprint(ynab.TransactionsApi().get_transactions(self.budget))
        except ApiException as e:
            print("Exception %s\n" % e)
            raise e
