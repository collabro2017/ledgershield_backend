from .http import Http

class Ethereum(Http):

    def __init__(self):
        # self.URL = 'http://13.58.248.113/ethapi'
        self.URL = 'http://localhost:8003'


    def getAccount(self):
        endpoint = 'wallet/new'
        return self.post(endpoint, data=None)

    def getDepositAmount(self, address):
        endpoint = 'wallet/balance/{}'.format(address)
        return self.get(endpoint)

    def transfer(self, outs):
        endpoint = 'wallet/transfer'
        return self.post(endpoint, outs)

    def buildUrl(self, endpoint):
        return "{}/{}".format(self.URL, endpoint )

    def get(self, endpoint):
        url = self.buildUrl(endpoint)
        return super().callget(url, None)

    def post(self, endpoint, data):
        url = self.buildUrl(endpoint)
        return super().callpost(url, data=data, auth=None)
