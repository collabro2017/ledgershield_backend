from asgiref.sync import async_to_sync
from celery.task import task
from channels.layers import get_channel_layer

from v1.blockchain.utils import Utils
from v1.coins.models import CoinPair
from v1.transactions.models import Transaction
import logging
import time

@task()
def wait_for_deposit(txid):
    logger = logging.getLogger(__name__)
    tx = Transaction.objects.get(pk=txid)
    address = tx.wallet_address
    coin = tx.deposit.symbol
    logger.info("Waiting for {} deposit for address {}".format( coin ,address))
    data, run = Utils.getWalletTransaction(address, coin)
    if run:
        logger.info("retry within 5 seconds!")
        time.sleep(5)
        wait_for_deposit.delay(txid)
    else:
        logger.info("{} received wallet data!".format(data))
        if 'hash' in data[0]:
            tx.deposit_tx_hash = data[0]['hash']
            tx.status = 'waiting_for_confirmation'
            tx.save()
            channel_name = 'txchannel-{}'.format(tx.order_id)
            chanel_layer = get_channel_layer()
            async_to_sync(chanel_layer.group_send)(channel_name, {
                'type': 'update.txinfo',
                'text': txid
            })
            watch_tx_confirmation.delay(txid)


@task()
def watch_tx_confirmation(txid, confirmations=0):
    logger = logging.getLogger(__name__)
    logger.info('tx {} - confirmations {}'.format(txid, confirmations))
    tx = Transaction.objects.get(pk=txid)

    data = Utils.getWalletTxDetail(tx.deposit_tx_hash)
    logger.info('tx hash {}'.format(tx.deposit_tx_hash))
    if data is not None:

        channel_name = 'txchannel-{}'.format(tx.order_id)
        chanel_layer = get_channel_layer()
        logger.info('channel name {}'.format(channel_name))
        if data['confirmations'] > confirmations:
            tx.deposit_tx_confirmations = data['confirmations']
            tx.save()
            async_to_sync(chanel_layer.group_send)(channel_name, {
                'type': 'update.txinfo',
                'text': txid
            })

        if data['confirmations'] >= 6:
            tx.status = 'deposit_received'
            tx.deposit_tx_confirmations = data['confirmations']
            tx.deposit_tx_amount = Utils.getDepositAmount(data['outputs'], tx.wallet_address)
            tx.save()

            async_to_sync(chanel_layer.group_send)(channel_name, {
                'type': 'update.txinfo',
                'text': txid
            })

            getExchangeRate.delay(txid)
        else:
            # TODO read retyr time from configuration specific to coin.
            time.sleep(60)
            watch_tx_confirmation.delay(txid, confirmations=data['confirmations'])
    else:
        # TODO read retry time from configuration specific to coin.
        time.sleep(10)
        watch_tx_confirmation.delay(tx.pk)



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
        tx.status  = 'awaiting'
        tx.wallet_address = address;
        tx.save();
        channel_name = 'txchannel-{}'.format(tx.order_id)
        chanel_layer = get_channel_layer()
        async_to_sync(chanel_layer.group_send)(channel_name, {
            'type':'update.txinfo',
            'text': txid
        })
        wait_for_deposit.delay(tx.pk)
    else:
        logger.warning("Something went wrong while generating deposit address!")

@task()
def getExchangeRate(txid):

    logger = logging.getLogger(__name__)

    tx = Transaction.objects.get(pk=txid)

    cp = CoinPair.objects.get(source=tx.deposit, destination=tx.withdraw)

    # cp.rate
    logger.info("Got Exhcnage Rate {}, service fee {}%".format(cp.rate, tx.deposit.service_fee))

    last_unit = tx.deposit_tx_amount / int(tx.deposit.decimals)

    logger.info("Converted in max unit {} and type {}".format(last_unit, type(last_unit)))

    fee = (last_unit  * tx.deposit.service_fee) / 100;

    exchange_amount = last_unit - fee;

    logger.info("Deducted Fee {}, Exchange {} amount {}".format(fee, tx.deposit.symbol, exchange_amount))

    dest_amount = exchange_amount * cp.rate

    logger.info("User will get {} {}".format(dest_amount, tx.withdraw.symbol))

    tx.exchange_rate = cp.rate;
    tx.save()

    channel_name = 'txchannel-{}'.format(tx.order_id)
    chanel_layer = get_channel_layer()
    async_to_sync(chanel_layer.group_send)(channel_name, {
        'type': 'update.txinfo',
        'text': txid
    })