from celery.task import task

from v1.blockchain.utils import Utils
from v1.transactions.models import Transaction
import logging

@task()
def wait_for_deposit(txid):
    Transaction.objects.get(pk=txid)

@task()
def get_deposit_address(txid):
    logger = logging.getLogger(__name__)
    tx = Transaction.objects.get(pk=txid)
    logger.debug("Transaction id {}".format(tx.pk))
    src = tx.deposit.symbol;
    dst = tx.withdraw.symbol;
    account_name = "{}-{}-{}".format(src, dst,tx.id);
    name, address = Utils.getDespositAddress(src, account_name)
    logger.debug("Got Address {} and accountname {}".format(address, account_name))
    if address is not None:
        tx.wallet_address = address;
        tx.save();
    else:
        logger.warning("Something went wrong while generating deposit address!")