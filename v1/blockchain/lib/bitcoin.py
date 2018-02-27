import requests

from .http import Http
import logging

logger = logging.getLogger(__name__)

class Bitcoin(Http):

    def __init__(self):
        self.URL = 'http://18.222.5.20:18332'
        self.APIKEY = '220b6e10-17df-11e8-b642-0ed5f89f718b'
        self.WALLETID = 'defaultwallet236'
        self.PASSPHRASE = 'this is dummy text, needs to be changed'
        self.NETWORK = 'network'

    def getNodeInfo(self):
        return self.get('/')

    def getWallet(self):
        endpoint = 'wallet/{}'.format(self.WALLETID)
        status, response = self.get(endpoint)
        if status == 404:
            logger.warning("WalletID {} doesn't exists, trying to create new wallet!".format(self.WALLETID))
            status, response = self.createWallet()
        return response;


    def createWallet(self):
        endpoint = 'wallet/{}'.format(self.WALLETID)
        data = {
            'witness': False,
            'passphrase': self.PASSPHRASE,
            'witness': True
        }
        return self.put(endpoint, data)

    def createAccount(self, accountname):
        endpoint = 'wallet/{}/account/{}'.format(self.WALLETID, accountname)
        data = {
            'type': 'pubkeyhash',
            'passphrase': self.PASSPHRASE,
            'witness': True
        }
        return self.put(endpoint, data)

    def getAccount(self, accountname):
        endpoint = 'wallet/{}/account/{}'.format(self.WALLETID, accountname)
        return self.get(endpoint)

    def getTxByAddress(self, address):
        endpoint ='tx/address/{}'.format(address)
        return self.get(endpoint)

    def getTxByHash(self, hash):
        endpoint = 'tx/{}'.format(hash)
        return self.get(endpoint)

    def getAuthObject(self):
        return requests.auth.HTTPBasicAuth('x', self.APIKEY)

    def buildUrl(self, endpoint):
        return "{}/{}".format(self.URL, endpoint )


    def get(self, endpoint):
        url = self.buildUrl(endpoint)
        auth = self.getAuthObject()
        return super().get(url, auth)

    def put(self, endpoint, data=None):
        url = self.buildUrl(endpoint)
        auth = self.getAuthObject()
        return super().put(url, auth, data)