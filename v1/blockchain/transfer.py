import logging

from v1.blockchain.lib.bitcoincash import BitcoinCash
from v1.blockchain.lib.ethereum import Ethereum

class Transfer:

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
