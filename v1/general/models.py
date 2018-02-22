from django.db import models

'''
    Abstract Timed model will created and modified column in the model.
'''


class TimedModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True