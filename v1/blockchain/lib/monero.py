from v1.blockchain.lib.http import Http
from django.conf import settings


class Monero(Http):
    def __init__(self):
        self.monero_settings = settings.BLOCKCHAIN_NODES['MONERO']
        self.URL = self.monero_settings['SERVER']

    def build_url(self, endpoint):
        return '{}/{}'.format(self.URL, endpoint)

    def get_address(self):
        endpoint = "wallet/new"
        return self.post(endpoint, None)

    def get_deposit_amount(self, payment_id):
        endpoint = "wallet/info/{}".format(payment_id)
        return self.get(endpoint)

    def transfer(self, outs):
        endpoint = 'wallet/transfer'
        return self.post(endpoint, outs)

    def get(self, endpoint):
        url = self.build_url(endpoint)
        return super().callget(url=url, auth=None)

    def post(self, endpoint, data):
        url = self.build_url(endpoint)
        return super().callpost(url=url, data=data, auth=None)


