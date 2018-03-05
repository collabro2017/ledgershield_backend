from datetime import datetime


def coins_image_upload_to(instance, filename):
    return "coins/{}".format(filename)

def transaction_status_choices():
    return (
        ('submitted','Submitted'),
        ('awaiting','Wating for deposit'),
        ('deposit_received','Deposit transaction received'),
        ('waiting_for_confirmation', 'Wating for transaction confirmation'),
        ('exchange', 'Exchanging'),
        ('out_order','Out of order'),
        ('completed', 'Completed')
    )