import logging

from v1.blockchain.lib.ethereum import Ethereum

class Transfer:

    @staticmethod
    def ETH(to, amount):

        logger = logging.getLogger(__name__)
        logger.info("Transfering {} ETH to address {}".format(amount, to))

        status, data = Ethereum().transfer(to, amount)

        if status == 200:
            logger.info("Txid {}".format(data['txid']))
            return data['txid']
        else:
            return None
