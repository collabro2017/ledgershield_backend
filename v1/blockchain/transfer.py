import logging

from v1.blockchain.lib.ethereum import Ethereum

class Transfer:

    @staticmethod
    def ETH(txid):

        logger = logging.getLogger(__name__)

        status, data = Ethereum().transfer(txid)
        if status == 200:
            logger.info("Txid {}".format(data['data']))
            return data['data']
        else:
            return None
