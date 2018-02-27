from datetime import datetime

from v1.blockchain.lib.bitcoin import Bitcoin
import logging

class Utils:
    @staticmethod
    def getDespositAddress(coin, accountname):
        logger = logging.getLogger(__name__)
        if coin.lower() == 'btc':
            status, response = Bitcoin().getAccount(accountname)
            logger.debug("1st {} =>  {}".format(status, response))
            if status == 404:
                status, response = Bitcoin().createAccount(accountname)
                logger.debug("2nd {} =>  {}".format(status, response))
            if status == 200:
                return (response['name'], response['receiveAddress'])

        return (accountname, None)

    @staticmethod
    def getAccountName(src, dst):
        return "{}-{}-{}".format(src, dst, datetime.now().timestamp())
