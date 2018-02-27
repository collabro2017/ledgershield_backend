from django.db import models

from v1.coins.models import Coin
from v1.general import utils as apputils
from v1.general.models import TimedModel


class Transaction(TimedModel):

    deposit = models.ForeignKey(Coin, related_name="deposit_coin", on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255, null=True)
    rollback_wallet = models.CharField(max_length=255)
    withdraw = models.ForeignKey(Coin, related_name="withdrawl_coin", on_delete=models.CASCADE)
    withdrawl_address = models.CharField(max_length=255)
    deposit_tx_hash = models.CharField(max_length=255, null=True)
    status = models.CharField(choices=apputils.transaction_status_choices(), max_length=10, db_index=True, default='submitted')
    note = models.TextField(max_length=255, null=True)


    class Meta:
        app_label = "transactions"


    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)

