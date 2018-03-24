from v1.blockchain.lib import http


class Ripple(http.Http):
    def __init__(self):
        self.URL = 'http://localhost:9002'

    def build_url(self, endpoint):
        return '{}/{}'.format(self.URL, endpoint)

    def callget(self, endpoint):
        endpoint = self.build_url(endpoint)
        return super().__get(endpoint, auth=None)

    def post(self, endpoint, data=None):
        endpoint = self.build_url(endpoint)
        return super().__post(endpoint, data, auth=None)

    def generate_wallet(self):
        endpoint = 'wallet/new'
        return self.post(endpoint)

    def get_account_info(self, address):
        endpoint = 'wallet/info/{}'.format(address)
        return self.callget(endpoint)

    def get_tx_detail(self, tx_hash):
        endpoint = 'wallet/tx/{}'.format(tx_hash)
        return self.callget(endpoint)

