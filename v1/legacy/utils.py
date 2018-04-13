
progress = {
    'submitted': {
        'progress': 25,
        'label': 'Transaction submitted',
        'cssClass': 'bg-info'
    },
    'awaiting': {
        'progress': 33.33,
        'label': 'Waiting for deposit',
        'cssClass': 'bg-info'
    },
    'waiting_for_confirmation': {
        'progress': 50,
        'label': 'Wating for confirmation',
        'cssClass': 'bg-info'

    },
    'deposit_received': {
        'progress': 66.66,
        'label': 'Deposit received',
        'cssClass': 'bg-info'
    },
    'exchange': {
        'progress': 83.33,
        'label': 'Exchanging',
        'cssClass': 'bg-info'
    },
    'completed': {
        'progress': 100,
        'label': 'All Done!',
        'cssClass': 'bg-success'
    },
    'out_order': {
        'progress': 83.33,
        'label': 'Out of order',
        'cssClass': 'bg-warning'
    }

}


def get_status(status):

    return progress[status]