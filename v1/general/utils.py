from datetime import datetime




def coins_image_upload_to(instance, filename):
    return "coins/{}".format(filename)

def transaction_status_choices():
    return (
        ('submitted','Submitted'),
        ('awaiting','Waiting for deposit'),
        ('deposit_received','Deposit received'),
        ('waiting_for_confirmation', 'Waiting for confirmation'),
        ('exchange', 'Exchanging'),
        ('out_order','Out of order'),
        ('completed', 'Completed'),
        ('refunded','Refunded'),
        ('partial_filled','Partially Filled')
    )
