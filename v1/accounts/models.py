from django.contrib.auth.models import AbstractUser
from django.db import models

from v1.general.models import TimedModel


class User(AbstractUser, TimedModel):

    email = models.EmailField(unique=True, db_index=True)

    class Meta:
        app_label = 'accounts'


    def __str__(self):
        return self.email

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)