import logging
import time

from asgiref.sync import async_to_sync
from celery.task import task
from channels.layers import get_channel_layer

from v1.blockchain.utils import Utils
from v1.coins.models import CoinPair
from v1.transactions.models import Transaction, TransactionOutputs
from v1.transactions.utils import get_pair_rates

# Step1::Generate Deposit Address
@task()
def get_deposit_address(txid):
    logger = logging.getLogger(__name__)
    tx = Transaction.objects.get(pk=txid)
    if tx.status == 'submitted':
        logger.debug("Transaction id {}".format(tx.pk))
        src = tx.deposit.symbol;
        dst = tx.withdraw.symbol;
        account_name = "{}-{}-{}".format(src, dst, tx.id);
        name, address, dt = Utils.get_desposit_address(src, account_name)
        logger.info("Got Address {} and accountname {}".format(address, account_name))
        if address is not None:
            tx.status = 'awaiting'
            tx.wallet_address = address;
            tx.exchange_rate = get_pair_rates(tx.deposit.pk, tx.withdraw.pk)
            if dt is not None:
                tx.destination_tag = dt
            tx.save();
            # channel_name = 'txchannel-{}'.format(tx.order_id)
            # chanel_layer = get_channel_layer()
            # async_to_sync(chanel_layer.group_send)(channel_name, {
            #     'type': 'update.txinfo',
            #     'text': txid
            # })
            wait_for_deposit.delay(tx.pk)
        else:
            logger.warning("Something went wrong while generating deposit address!")
    else:
        logger.warning("Tx {} at invalid step, to get the deposit address! ".format(txid))


# Step2::Waiting for deposit
@task()
def wait_for_deposit(txid):
    logger = logging.getLogger(__name__)
    tx = Transaction.objects.get(pk=txid)
    if tx.status == 'awaiting':
        address = tx.wallet_address
        logger.info("Waiting for {} deposit for address {} tx {}".format(tx.deposit.symbol, address, txid))
        data, run = Utils.get_wallet_transaction(tx)
        logger.info(data)
        if run:
            logger.info("retry within 5 seconds!")
            time.sleep(5)
            wait_for_deposit.delay(txid)
            return
        else:
            logger.info("{} received wallet data!".format(data))
            tx.deposit_tx_hash = data['hash']
            tx.deposit_tx_amount = data['amount']
            tx.status = 'waiting_for_confirmation'
            tx.exchange_rate = get_pair_rates(tx.deposit.pk, tx.withdraw.pk)
            tx.save()
            # channel_name = 'txchannel-{}'.format(tx.order_id)
            # chanel_layer = get_channel_layer()
            # async_to_sync(chanel_layer.group_send)(channel_name, {
            #     'type': 'update.txinfo',
            #     'text': txid
            # })
            wait_for_tx_confirmation.delay(txid)
            return
    else:
        logger.warning("Tx {} at invalid step {}! ".format(txid, tx.status))


# Step3:: Wait for tx confirmations at-least 6
@task()
def wait_for_tx_confirmation(txid):
    logger = logging.getLogger(__name__)
    tx = Transaction.objects.get(pk=txid)
    logger.info('tx [{}] - confirmations [{}]- status [{}]'.format(txid, tx.deposit_tx_confirmations, tx.status))
    if tx.status == 'waiting_for_confirmation':
        data = Utils.get_wallet_tx_detail(tx, tx.deposit)
        if data is not None:
            exchange_rate = get_pair_rates(tx.deposit.pk, tx.withdraw.pk)
            deposit_confirmations = data['confirmations']
            # channel_name = 'txchannel-{}'.format(tx.order_id)
            # chanel_layer = get_channel_layer()
            if deposit_confirmations >= 6:
                tx.status = 'deposit_received'
                tx.exchange_rate = exchange_rate
                tx.deposit_tx_confirmations = deposit_confirmations
                tx.save()
                # async_to_sync(chanel_layer.group_send)(channel_name, {
                #     'type': 'update.txinfo',
                #     'text': txid
                # })
                get_exchange_rate.delay(txid)
            else:

                tx.exchange_rate = exchange_rate
                tx.deposit_tx_confirmations = deposit_confirmations
                tx.save()

                # async_to_sync(chanel_layer.group_send)(channel_name, {
                #     'type': 'update.txinfo',
                #     'text': txid
                # })

                # TODO:: Retry time from configuration specific to coin.
                time.sleep(60)
                wait_for_tx_confirmation.delay(txid)
        else:
            # TODO:: Retry time from configuration specific to coin.
            time.sleep(10)
            wait_for_tx_confirmation.delay(tx.pk)
    else:
        logger.warning("Tx {} at invalid step {} ! ".format(txid, tx.status))


# Step4::Get exchange rate and calculate service fee.
@task()
def get_exchange_rate(txid):
    logger = logging.getLogger(__name__)
    tx = Transaction.objects.get(pk=txid)
    if tx.status == 'deposit_received':
        cp = CoinPair.objects.get(source=tx.deposit, destination=tx.withdraw)
        logger.info("Got Exhcnage Rate {}, service fee {}%".format(cp.rate, tx.deposit.service_fee))

        tx_deposit_decimals = int(tx.deposit.decimals)

        last_unit = 1;
        if tx_deposit_decimals > 0:
            last_unit = tx.deposit_tx_amount / int(tx.deposit.decimals)

        logger.info("Converted in max unit {} and type {}".format(last_unit, type(last_unit)))
        # Calculating service fee
        fee = (last_unit * tx.deposit.service_fee) / 100;
        # Subtracting service fee form exchanged amount.
        exchange_amount = last_unit - fee;
        logger.info("Deducted Fee {}, Exchange {} amount {}".format(fee, tx.deposit.symbol, exchange_amount))
        # Getting the final exchanged amount.
        dest_amount = exchange_amount * cp.rate

        logger.info("User will get {} {}".format(dest_amount, tx.withdraw.symbol))

        # Saving tx information
        tx.exchange_rate = cp.rate
        tx.withdraw_amount = dest_amount
        tx.status = 'exchange'
        tx.save()

        # Updating client via socket
        # channel_name = 'txchannel-{}'.format(tx.order_id)
        # chanel_layer = get_channel_layer()
        # async_to_sync(chanel_layer.group_send)(channel_name, {
        #     'type': 'update.txinfo',
        #     'text': txid
        # })
        transfer_exchanged_amount.delay(txid)


# Step5::Transfer exchanged amount
@task()
def transfer_exchanged_amount(txid):
    logger = logging.getLogger(__name__)
    tx = Transaction.objects.get(pk=txid)
    if tx.status == 'exchange':
        data = Utils.transfer_exchanged_amount(txid, tx.withdraw)
        status = 'completed'
        note = 'All done!'

        if data is not None:
            for item in data:
                tx_out = TransactionOutputs.objects.get(pk=item['id'])
                if 'tx_hash' in item:
                    tx_out.tx_hash = item['tx_hash']
                else:
                    tx_out.tx_hash = ''

                tx_out.amount = item['amount']
                if 'comment' in item:
                    tx_out.comment = item['comment']
                else:
                    tx_out.comment = ''

                tx_out.save()
                if not tx_out.tx_hash:
                    status = 'out_order';
                    note = tx_out.comment

            tx.status = status
            tx.note = note
            tx.save()
        else:
            tx.status = 'out_order'
            tx.note = 'Something went wrong while transferring your withdrawn amount, please contact to support center to further assistance!';
            tx.save()

        # channel_name = 'txchannel-{}'.format(tx.order_id)
        # chanel_layer = get_channel_layer()
        # async_to_sync(chanel_layer.group_send)(channel_name, {
        #     'type': 'update.txinfo',
        #     'text': txid
        # })
    else:
        logger.warning("Tx {} at invalid step {}! ".format(txid, tx.status))


# Step6::Refund Remaining amount
@task()
def refund_task(txid):
    tx = Transaction.objects.get(pk=txid)
    logger = logging.getLogger('Refund Task')
    if tx.status == 'out_order':
        data = Utils.refund_remain_amount(tx)
        status = 'refunded'
        note = 'All Done!'

        if data is not None:
            for item in data:
                tx_out = TransactionOutputs.objects.get(pk=item['id'])
                if 'tx_hash' in item:
                    tx_out.tx_hash = item['tx_hash']
                else:
                    tx_out.tx_hash = ''

                tx_out.amount = item['amount']
                if 'comment' in item:
                    tx_out.comment = item['comment']
                else:
                    tx_out.comment = ''

                tx_out.save()
                if not tx_out.tx_hash:
                    status = 'out_order';
                    note = tx_out.comment

            tx.status = status
            tx.note = note
            tx.save()
        else:
            tx.status = 'out_order'
            tx.note = 'Something went wrong while refunding your amount, please contact to support center to further assistance!';
            tx.save()

        # channel_name = 'txchannel-{}'.format(tx.order_id)
        # chanel_layer = get_channel_layer()
        # async_to_sync(chanel_layer.group_send)(channel_name, {
        #     'type': 'update.txinfo',
        #     'text': txid
        # })
    else:
        logger.warning('Tx {} at invalid step {}!'.format(txid, tx.status))

