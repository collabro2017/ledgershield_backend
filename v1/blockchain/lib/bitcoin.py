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
        self.NETWORK = 'testnet'

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
            'passphrase': self.PASSPHRASE,
            'witness': True
        }
        return self.put(endpoint, data)

    def createAccount(self, accountname):
        endpoint = 'wallet/{}/account/{}'.format(self.WALLETID, accountname)
        data = {
            'type': 'multisig',
            'passphrase': self.PASSPHRASE,
            'witness': True,
            'network': self.NETWORK
        }
        return self.put(endpoint, data)

    def getAccount(self, accountname):
        endpoint = 'wallet/{}/account/{}'.format(self.WALLETID, accountname)
        return self.get(endpoint)

    def getTxByAddress(self, address):
        endpoint = 'tx/address/{}'.format(address)
        return self.get(endpoint)

    def getTxByHash(self, hash):
        endpoint = 'tx/{}'.format(hash)
        return self.get(endpoint)

    def getAuthObject(self):
        return requests.auth.HTTPBasicAuth('x', self.APIKEY)

    def buildUrl(self, endpoint):
        return "{}/{}".format(self.URL, endpoint)

    def getWalletTxDetail(self, txhash):
        endpoint = "wallet/{}/tx/{}".format(self.WALLETID, txhash)
        return self.get(endpoint)

    def sendTransaction(self, data):
        data['passphrase'] = self.PASSPHRASE
        endpoint = 'wallet/{}/send'.format(self.WALLETID)
        return self.post(endpoint, data)

    def rpc(self, data):
        url = self.buildUrl('')
        auth = self.getAuthObject()
        return super().post(url, data, auth)

    def post(self, endpoint, data):
        url = self.buildUrl(endpoint)
        auth = self.getAuthObject()
        return super().post(url, data, auth)

    def get(self, endpoint):
        url = self.buildUrl(endpoint)
        auth = self.getAuthObject()
        return super().get(url, auth)

    def put(self, endpoint, data=None):
        url = self.buildUrl(endpoint)
        auth = self.getAuthObject()
        return super().put(url, auth, data)

    @staticmethod
    def normalize_tx(data, address):
        if len(data) > 0:
            if 'hash' in data[0]:
                hash = data['hash']
                amount = 0;
                for out in data[0]['outputs']:
                    if out['address'] == address:
                        amount = out['value']
                        break
                return hash, amount
        return None, None
