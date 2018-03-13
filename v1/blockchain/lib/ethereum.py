from .http import Http

class Ethereum(Http):

    def __init__(self):
        self.URL = 'http://13.58.248.113/ethapi'


    def transfer(self, to , amount):
        endpoint = 'wallet/transfer/{}/{}'.format(to,amount)
        return self.get(endpoint)

    def buildUrl(self, endpoint):
        return "{}/{}".format(self.URL, endpoint )

    def get(self, endpoint):
        url = self.buildUrl(endpoint)

        return super().get(url, None)
