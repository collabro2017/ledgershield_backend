from django.db import models

from v1.general.models import TimedModel
from v1.general import  utils as apputils

class Coin(TimedModel):
    name = models.CharField(db_index=True, unique=True, max_length=50)
    symbol = models.CharField(db_index=True, unique=True, max_length=30)
    image = models.ImageField(upload_to=apputils.coins_image_upload_to, null=True)
    operational = models.BooleanField(default=False)
    service_fee = models.FloatField(default=0)
    decimals = models.CharField(default=0, max_length=30)
    # fee_per_kb = models.PositiveIntegerField(default=0)
    multi_withdrawal = models.BooleanField(default=False)
    block_explorer_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get(self):
        return self;

    class Meta:
        ordering = ['pk','-operational']


class CoinPair(TimedModel):
    source = models.ForeignKey(Coin, related_name="source_coin", on_delete=models.CASCADE)
    destination = models.ForeignKey(Coin, related_name="destination_coin", on_delete=models.CASCADE)
    rate = models.FloatField()
    minerFee = models.FloatField(default=0)

    class Meta:
        ordering = ['source__symbol']