from django.db import models

from v1.general.models import TimedModel
from v1.general import  utils as apputils

class Coin(TimedModel):
    name = models.CharField(db_index=True, unique=True, max_length=50)
    symbol = models.CharField(db_index=True, unique=True, max_length=30)
    image = models.ImageField(upload_to=apputils.coins_image_upload_to, null=True)
    api_url = models.URLField()
    api_auth = models.BooleanField(default=True)
    api_username = models.CharField(max_length=32)
    api_password = models.CharField(max_length=64)
    deposit_endpoint = models.CharField(max_length=255)
    withdraw_endpoint = models.CharField(max_length=255)
    operational = models.BooleanField(default=False)

    def __str__(self):
        return self.name