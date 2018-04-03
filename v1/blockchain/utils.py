from datetime import datetime

from django.forms import model_to_dict

from v1.blockchain.lib.bitcoin import Bitcoin
import logging

from v1.blockchain.lib.bitcoincash import BitcoinCash
from v1.blockchain.lib.ethereum import Ethereum
from v1.blockchain.lib.ripple import Ripple
from v1.blockchain.transfer import Transfer
from v1.transactions.models import Transaction
from v1.transactions.serializers import TransactionDetailSerializer, TransactionOutsSerializer


class Utils:
    @staticmethod
    def get_desposit_address(coin, accountname):
        logger = logging.getLogger(__name__)
        if coin.lower() == 'btc':
            status, response = Bitcoin().getAccount(accountname)
            logger.debug("1st {} =>  {}".format(status, response))
            if status == 404:
                status, response = Bitcoin().createAccount(accountname)
                logger.debug("2nd {} =>  {}".format(status, response))
            if status == 200:
                return response['name'], response['nestedAddress'], None
        elif coin.lower() == 'eth':
            status, response = Ethereum().getAccount()
            if status == 200:
                return None, response['address'], None
        elif coin.lower() == 'xrp':
            status, data = Ripple().generate_wallet()
            logger.info(data)
            if status == 201:
                return accountname, data['address'], data['dt']
            return accountname, None, None
        elif coin.lower() == 'bch':
            status, data = BitcoinCash().generate_wallet()
            if status == 201:
                logger.info('{}'.format(data))
                return accountname, data['lagacy'], None

        return accountname, None, None

    @staticmethod
    def get_account_name(src, dst):
        return "{}-{}-{}".format(src, dst, datetime.now().timestamp())

    @staticmethod
    def getTxByHash(hash):
        status, data = Bitcoin().getTxByHash(hash)

        if status == 200:
            return data
        return None

    @staticmethod
    def get_wallet_transaction(tx):
        address = tx.wallet_address
        logger = logging.getLogger(__name__)
        coin_name = tx.deposit.symbol.lower()
        if coin_name == 'btc':
            status, data = Bitcoin().getTxByAddress(address)
            if status == 200:
                logger.info('{}'.format(data))
                if len(data) == 0:
                    return None, True
                hash, amount = Bitcoin.normalize_tx(data, address)
                return {'hash': hash, 'amount': amount}, False
            else:
                return None, True
        elif coin_name == 'eth':
            status, response  = Ethereum().getDepositAmount(address)

            if status == 200:
                # TODO :: Need to find a way to get the transaction hash of ethereum deposit.
                if response['balance'] <=0 :
                    return None, True

                return {'hash': '--NONE--', 'amount': response['balance'] }, False
            return None, True

        elif coin_name == 'bch':
            status, response = BitcoinCash().get_balance_by_address(address, 0)
            logger.info('{} {}'.format(status, response))
            if status == 200:
                if response['balance'] <=0:
                    return None, True
                return {'hash': '--NONE--', 'amount': response['balance']}, False

        elif coin_name == 'xrp':
            status, response = Ripple().get_balance_by_dt(tx.destination_tag)
            if status == 200:
                balance = float(response['balance'])
                tx_hash = response['hash']
                logger.info("Balance {} Hash {}".format(balance, tx_hash))
                if balance <=0:
                    return None, True
                return {'hash': tx_hash,  'amount': balance}, False
            else:
                return None, True

        else:
            logger.warning("{} is not supported yet!".format(coin_name))

        return None, False

    @staticmethod
    def get_wallet_tx_detail(tx, coin):
        logger = logging.getLogger('Wallet')
        coin_name = coin.symbol.lower()
        tx_hash =  tx.deposit_tx_hash
        if coin_name == 'btc':
            st, data = Bitcoin().getWalletTxDetail(tx_hash)
            if st == 200:
                return data
            return None
        elif coin_name == 'eth':
            # TODO :: Need to get confirmations from the ethereum node.
            return {'confirmations': 6}
        elif coin_name == 'bch':
            st, data = BitcoinCash().get_balance_by_address(address=tx.wallet_address, confirmations=6)
            if st == 200:
                if data['balance'] <= 0:
                    return None
                return {'confirmations': 6}
            return None
        elif coin_name == 'xrp':
            st, data = Ripple().get_tx_detail(tx_hash)
            if st == 200:
                if 'outcome' in data:
                    # tx = Transaction.objects.get(deposit_tx_hash=tx_hash, deposit__symbol= coin)
                    amount = float(data['outcome']['deliveredAmount']['value'])
                    logger.info('{} {}'.format(tx.deposit_tx_amount, amount))
                    if tx.deposit_tx_amount == amount:
                        return {'confirmations': 6}
            return None

    @staticmethod
    def get_deposit_amount(outs, address):
        amount = 0;

        for out in outs:
            if out['address'] == address:
                amount =  out['value']
                break
        return amount

    @staticmethod
    def calculate_amount_share(outs, total_amount):
        logger = logging.getLogger(__name__)
        outputs = []
        for out in outs:
            o = dict(out)
            if not o['tx_hash']:
                logger.info('{}'.format(o))
                o['amount'] = total_amount * o['value'] / 100
                outputs.append(o)

        return outputs

    @staticmethod
    def transfer_exchanged_amount(txid, coin):
        coin_name = coin.symbol.lower()
        tx = Transaction.objects.get(pk=txid)
        tx_out = TransactionOutsSerializer(tx).data
        outs = Utils.calculate_amount_share(tx_out['outs'], tx.withdraw_amount)
        if coin_name == 'btc':
            return Transfer.BTC(outs)
        elif coin_name == 'eth':
            return Transfer.ETH(outs)
        elif coin_name == 'bch':
            return Transfer.BCH(outs)
        elif coin_name == 'xrp':
            return Transfer.XRP(outs)

        return None

    @staticmethod
    def get_refund_outputs(tx_outs):
        outs = []
        for out in tx_outs:
            o = dict(out)
            if not o['tx_hash']:
                outs.append(o)
        return outs;

    @staticmethod
    def refund_remain_amount(tx):
        coin_name = tx.withdraw.symbol.lower()
        serialized_tx = TransactionOutsSerializer(tx).data
        outs = Utils.get_refund_outputs(serialized_tx['outs'])

        if coin_name == 'btc':
            return Transfer.BTC(outs)
        elif coin_name == 'eth':
            return Transfer.ETH(outs)
        elif coin_name == 'xrp':
            return Transfer.XRP(outs)
        elif coin_name == 'bch':
            return Transfer.BCH(outs)

        return None;
