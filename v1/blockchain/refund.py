
from v1.transactions.models import Transaction
from v1.blockchain.lib.bitcoin import Bitcoin

class Refund:

    def Bitcoin(self, txid):

        tx = Transaction.objects.get(pk=txid)
        data = {
            'rate': 1000,
            'subtractFee': True,
            'depth': 6,
            'outputs': [
                {'address': tx.rollback_wallet, 'value': tx.deposit_tx_amount }
            ]
        }

        btc = Bitcoin()
        st, data = btc.sendTransaction(data)
        return data;
