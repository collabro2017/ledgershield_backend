import logging

from v1.blockchain.lib.bitcoin import Bitcoin
from v1.blockchain.lib.bitcoincash import BitcoinCash
from v1.blockchain.lib.ethereum import Ethereum
from v1.blockchain.lib.monero import Monero
from v1.blockchain.lib.ripple import Ripple


class Address:

    def __init__(self, account_name):
        self.account_name = account_name
        self.logger = logging.getLogger('deposit_address')

    def BTC(self):
        status, response = Bitcoin().getAccount(self.account_name)
        self.logger.debug("1st {} =>  {}".format(status, response))
        if status == 404:
            status, response = Bitcoin().createAccount(self.account_name)
            self.logger.debug("2nd {} =>  {}".format(status, response))
        if status == 200:
            return response['name'], response['nestedAddress'], None

        return self.account_name, None, None

    def ETH(self):
        status, response = Ethereum().getAccount()
        if status == 200:
            return None, response['address'], None

        return self.account_name, None, None

    def BCH(self):
        status, response = BitcoinCash().generate_wallet()
        if status == 201:
            return self.account_name, response['lagacy'], None

        return self.account_name, None, None

    def XRP(self):
        status, response = Ripple().generate_wallet()
        if status == 201:
            return self.account_name, response['address'], response['dt']
        return self.account_name, None, None

    def XMR(self):
        status, response = Monero().get_address()
        if status == 200:
            if 'integrated_address' in response and 'payment_id' in response:
                return self.account_name, response['integrated_address'], response['payment_id']

        return self.account_name, None, None
