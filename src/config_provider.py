# Config Keys
USERNAME = "username"
PASSWORD = "password"
SERVER = "server"
PORT = "port"
API_KEY = "ynab_api_key"
BUDGET = "ynab_budget"
ACCOUNT = "ynab_account"


class ConfigProvider(object):

    def __init__(self, config_pairs):
        self.config = config_pairs

    def api_key(self):
        return self.config[API_KEY]

    def budget_id(self):
        return self.config[BUDGET]

    def server(self):
        return self.config[SERVER]

    def port(self):
        return self.config[PORT]

    def username(self):
        return self.config[USERNAME]

    def password(self):
        return self.config[PASSWORD]

    def account(self):
        return self.config[ACCOUNT]
