from django.shortcuts import render
from v1.transactions.models import Transaction
from v1.legacy.utils import get_status

def index(request, order_id):
    tx = Transaction.objects.get(order_id=order_id)

    tx_status = get_status(tx.status)
    return render(request, 'transaction.html', {
        'tx': tx,
        'tx_status': tx_status
    });