from datetime import datetime


def coins_image_upload_to(instance, filename):
    return "coins/{}-{}".format(datetime.now().timestamp(), filename)

def transaction_status_choices():
    return (
        ('submitted','Submitted'),
        ('awaiting','Wating for deposit'),
        ('deposit_received','Deposit transaction received'),
        ('exchange', 'Exchanging'),
        ('out_order','Out of order'),
        ('completed', 'Completed')
    )