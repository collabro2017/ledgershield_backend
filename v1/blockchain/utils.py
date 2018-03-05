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
                logger.info(response)
                return (response['name'], response['nestedAddress'])

        return (accountname, None)

    @staticmethod
    def getAccountName(src, dst):
        return "{}-{}-{}".format(src, dst, datetime.now().timestamp())

    @staticmethod
    def getTxByHash(hash):
        status, data = Bitcoin().getTxByHash(hash)

        if status == 200:
            return data
        return None

    @staticmethod
    def getWalletTransaction(address, coin):
        logger = logging.getLogger(__name__)
        if coin.lower() == 'btc':
            status, data = Bitcoin().getTxByAddress(address)
            if status == 200:
                if len(data) == 0:
                    return (None, True)

                return (data, False)
            else:
                return (None, True)
        else:
            logger.warning("{} is not supported yet!".format(coin))

        return (None, False)

    @staticmethod
    def getWalletTxDetail(txhash):
        st, data = Bitcoin().getWalletTxDetail(txhash)
        if st == 200:
            return data
        return None

    @staticmethod
    def getDepositAmount(outs, address):
        amount = 0;
        for out in outs:
            if out['address'] == address:
                amount =  out['value']
                break
        return amount