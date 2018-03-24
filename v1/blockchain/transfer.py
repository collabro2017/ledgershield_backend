import logging

from v1.blockchain.lib.bitcoin import Bitcoin
from v1.blockchain.lib.bitcoincash import BitcoinCash
from v1.blockchain.lib.ethereum import Ethereum

class Transfer:

    @staticmethod
    def BTC(outs):
        logger = logging.getLogger(__name__)
        outputs = []
        for out in outs:
            outputs.append({'address': out['address'], 'value': int(out['amount'] * 100000000)})

        data = {
            'rate': 1000,
            'subtractFee': True,
            'depth': 6,
            'outputs': outputs
        }
        logger.info('{}'.format(data))
        btc = Bitcoin()
        st, response = btc.sendTransaction(data)
        logger.info('{} {}'.format(st, data))
        if st ==200 and 'hash' in response:
            outputs = []
            for obj in outs:
                out = obj.copy()
                out.update({'tx_hash': response['hash'], 'comment': '' })
                outputs.append(out)
            return outputs
        else:
            return None


    @staticmethod
    def ETH(outs):

        logger = logging.getLogger(__name__)
        status, data = Ethereum().transfer(outs)
        if status == 200:
            logger.info("Transfer TX ETH response {}".format(data['data']))
            return data['data']
        else:
            return None
    @staticmethod
    def BCH(outs):
        logger = logging.getLogger(__name__)
        status, data = BitcoinCash().transfer(outs)
        if status == 200:
            logger.info("Transfer TX BCH response {}".format(data))
            return data
        else:
            return None
