from django.db import models

from v1.general.models import TimedModel
from v1.general import  utils as apputils

class Coin(TimedModel):
    name = models.CharField(db_index=True, unique=True, max_length=50)
    symbol = models.CharField(db_index=True, unique=True, max_length=30)
    image = models.ImageField(upload_to=apputils.coins_image_upload_to, null=True)
    operational = models.BooleanField(default=False)
    price_btc = models.DecimalField(decimal_places=18, max_digits=24, default=0)

    def __str__(self):
        return self.name

    def get(self):
        return self;
