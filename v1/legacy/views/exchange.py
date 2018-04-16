from django.shortcuts import render, redirect
from v1.coins.models import CoinPair, Coin
from v1.legacy.forms import TransactionForm
from v1.transactions.models import Transaction, TransactionOutputs

def validate(context):
    outs = int(context['outs'])



def index(request, deposit):
    symbol = deposit.upper()
    pairs = CoinPair.objects.filter(source__symbol=symbol)
    if request.method == 'POST':

        if request.POST.get("add_more"):
            outs = int(request.POST['outs']) +1
            context = request.POST.copy()
            context['outs']= outs
            form = TransactionForm(context)
            return render(request, 'exchange_form.html', {
                'pairs': pairs,
                'form': form,
                'outs': range(0, outs),
                'context': context
            });
        else:
            try:
                context = request.POST
                outs = int(request.POST['outs'])
                tx_outs = []

                for i in range(outs):
                    address = context['dest_addr_{}'.format(i)]
                    value = context['dest_amount_{}'.format(i)]
                    tx_out = TransactionOutputs()
                    tx_out.address = address
                    tx_out.value = value
                    tx_out.save()
                    tx_outs.append(tx_out)

                tx = Transaction()
                tx.deposit = Coin.objects.get(pk=context['deposit'])
                tx.withdraw = Coin.objects.get(pk=context['withdraw'])
                tx.rollback_wallet = context['rollback_wallet']
                tx.save()
                tx.outs.set(tx_outs)
                tx.save()
                return redirect('txstatus',order_id=tx.order_id)

            except Exception as ex:
                print(ex)
                return redirect('/error')
    else:
        form = TransactionForm()
        return render(request, 'exchange_form.html', {
            'pairs': pairs,
            'form': form,
            'outs': range(0,1)
        });
