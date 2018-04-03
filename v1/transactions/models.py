import uuid

from django.db import models

from v1.coins.models import Coin
from v1.general import utils as apputils
from v1.general.models import TimedModel


class TransactionOutputs(models.Model):
    address = models.CharField(max_length=200)
    value = models.FloatField()
    amount = models.FloatField(default=0)
    tx_hash = models.CharField(max_length=255, null=True)
    comment = models.TextField(null=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return "{} -> {}".format(self.address, self.value)


class Transaction(TimedModel):
    order_id = models.UUIDField(default=uuid.uuid4)
    deposit = models.ForeignKey(Coin, related_name="deposit_coin", on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255, null=True)
    destination_tag = models.PositiveIntegerField(default=0, null=True, blank=True)
    rollback_wallet = models.CharField(max_length=255)
    deposit_tx_hash = models.CharField(max_length=255, null=True, blank=True)
    deposit_tx_amount =  models.FloatField(default=0)
    deposit_tx_confirmations = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=apputils.transaction_status_choices(), max_length=100, db_index=True, default='submitted')
    note = models.TextField(max_length=255, null=True, blank=True)
    exchange_rate = models.FloatField(default=0)
    withdraw = models.ForeignKey(Coin, related_name="withdrawal_coin", on_delete=models.CASCADE)
    withdraw_amount = models.FloatField(default=0)
    outs = models.ManyToManyField(TransactionOutputs, related_name="transaction_outputs")

    class Meta:
        app_label = "transactions"
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)
