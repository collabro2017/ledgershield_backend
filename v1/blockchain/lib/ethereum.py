from v1.transactions.models import Transaction
from .http import Http

class Ethereum(Http):

    def __init__(self):
        self.URL = 'http://127.0.0.1:8000'

    def getAccount(self):
        endpoint = 'wallet/new'
        return self.post(endpoint, data=None)

    def transfer(self, txid):
        tx = Transaction.objects.get(pk=txid)
        endpoint = 'wallet/transfer'
        return self.post(endpoint, tx.outs)

    def buildUrl(self, endpoint):
        return "{}/{}".format(self.URL, endpoint )

    def get(self, endpoint):
        url = self.buildUrl(endpoint)

        return super().get(url, None)

    def post(self, endpoint, data):
        url = self.buildUrl(endpoint)
        return super().post(url, data=data, auth=None)
