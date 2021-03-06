from v1.blockchain.lib import http


class Ripple(http.Http):
    def __init__(self):
        self.URL = 'http://localhost:9002'

    def build_url(self, endpoint):
        return '{}/{}'.format(self.URL, endpoint)

    def get(self, endpoint):
        endpoint = self.build_url(endpoint)
        return super().callget(endpoint, auth=None)

    def post(self, endpoint, data=None):
        endpoint = self.build_url(endpoint)
        return super().callpost(endpoint, data, auth=None)

    def get_balance_by_dt(self, dt):
        endpoint = 'wallet/dt/{}'.format(dt)
        return self.get(endpoint)

    def generate_wallet(self):
        endpoint = 'wallet/new'
        return self.post(endpoint)

    def get_account_info(self, address):
        endpoint = 'wallet/info/{}'.format(address)
        return self.get(endpoint)

    def get_tx_detail(self, tx_hash):
        endpoint = 'wallet/tx/{}'.format(tx_hash)
        return self.get(endpoint)

    def transfer(self, outs):
        endpoint = 'wallet/transfer'
        return self.post(endpoint, data=outs)

