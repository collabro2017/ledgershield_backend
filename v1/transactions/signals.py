from django.db.models.signals import post_save
from django.dispatch import receiver
from v1.transactions.models import Transaction
from v1.transactions.tasks import get_deposit_address

@receiver(post_save, sender=Transaction)
def on_transaction_save(sender, instance, **kwargs):
    if kwargs['created']:
        get_deposit_address.delay(instance.id)