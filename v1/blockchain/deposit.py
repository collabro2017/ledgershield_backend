import logging

from v1.blockchain.lib.bitcoin import Bitcoin
from v1.blockchain.lib.bitcoincash import BitcoinCash
from v1.blockchain.lib.ethereum import Ethereum
from v1.blockchain.lib.monero import Monero
from v1.blockchain.lib.ripple import Ripple


class Deposit:

    def __init__(self, address, tag):
        self.tag = tag
        self.address = address
        self.logger = logging.getLogger("deposit_info")

    def BTC(self):
        status, data = Bitcoin().getTxByAddress(self.address)
        if status == 200:
            if len(data) == 0:
                return None, True
            tx_hash, amount = Bitcoin.normalize_tx(data, self.address)
            return {'hash': tx_hash, 'amount': amount}, False

        return None, True

    def ETH(self):
        status, response = Ethereum().getDepositAmount(self.address)

        if status == 200:
            # TODO :: Need to find a way to get the transaction hash of ethereum deposit.
            if response['balance'] <= 0:
                return None, True

            return {'hash': '--NONE--', 'amount': response['balance']}, False
        return None, True

    def BCH(self):
        status, response = BitcoinCash().get_balance_by_address(self.address, 0)
        if status == 200:
            if response['balance'] <= 0:
                return None, True
            return {'hash': '--NONE--', 'amount': response['balance']}, False

    def XRP(self):
        status, response = Ripple().get_balance_by_dt(self.tag)
        if status == 200:
            balance = float(response['balance'])
            tx_hash = response['hash']
            self.logger.info("Balance {} Hash {}".format(balance, tx_hash))
            if balance <= 0:
                return None, True
            return {'hash': tx_hash, 'amount': balance}, False
        else:
            return None, True

    def XMR(self):
        status, response = Monero().get_deposit_amount(self.tag)
        if status == 200:
            if 'amount' in response and 'tx_hash' in response:
                tx_amount = response['amount']
                tx_hash = response['tx_hash']
                return {'hash': tx_hash, 'amount': tx_amount}
        return None, True
