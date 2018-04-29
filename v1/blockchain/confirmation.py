import logging

from v1.blockchain.lib.bitcoin import Bitcoin
from v1.blockchain.lib.bitcoincash import BitcoinCash
from v1.blockchain.lib.monero import Monero
from v1.blockchain.lib.ripple import Ripple


class Confirmation:

    def __int__(self, tx):
        self.tx = tx
        self.logger = logging.getLogger('wallet_confirmations')
        self.tx_hash = self.tx.deposit_tx_hash
        self.deposit_amount = self.tx.deposit_tx_amount

    def BTC(self):
        st, data = Bitcoin().getWalletTxDetail(self.tx_hash)
        if st == 200:
            return data
        return None

    def ETH(self):
        # TODO :: Need to get confirmations from the ethereum node.
        return {'confirmations': 6}

    def BCH(self):
        st, data = BitcoinCash().get_balance_by_address(address=self.tx.wallet_address, confirmations=6)
        if st == 200:
            if data['balance'] <= 0:
                return None
            return {'confirmations': 6}
        return None

    def XRP(self):
        st, data = Ripple().get_tx_detail(self.tx_hash)
        if st == 200:
            if 'outcome' in data:
                amount = float(data['outcome']['deliveredAmount']['value'])
                self.logger.info('{} {}'.format(self.deposit_amount, amount))
                if self.deposit_amount == amount:
                    return {'confirmations': 6}
        return None

    def XMR(self):
        return {'confirmations': 6}
