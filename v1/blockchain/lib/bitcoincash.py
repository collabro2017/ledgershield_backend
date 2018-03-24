from v1.blockchain.lib import http


class BitcoinCash(http.Http):

    def __init__(self):
        self.base_url = 'http://localhost:9003'

    def generate_wallet(self):
        endpoint = 'wallet/new'
        return self.post(endpoint)

    def get_balance_by_address(self, address, confirmations=0):
        endpoint = 'wallet/balance/{}/{}'.format(address, confirmations)
        return self.callget(endpoint)

    def build_url(self, endpoint):
        return '{}/{}'.format(self.base_url, endpoint)

    def post(self, endpoint, data=None):
        url = self.build_url(endpoint)
        return super().callpost(url, data, auth=None)

    def callget(self, endpoint):
        url = self.build_url(endpoint)
        return super().callget(url, auth=None)

    def transfer(self, outs):
        endpoint = 'wallet/transfer'
        return self.post(endpoint, outs)