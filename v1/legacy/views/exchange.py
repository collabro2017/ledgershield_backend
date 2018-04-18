import math

from django.shortcuts import render, redirect
from v1.coins.models import CoinPair, Coin
from v1.legacy.forms import TransactionForm
from v1.transactions.models import Transaction, TransactionOutputs


def validate(context):
    outs = int(context['outs'])
    total_sum = 0;
    errors = {
        'outs':[],
        'over100': '',
        'deposit': '',
        'withdraw':'',
        'rollback_wallet': ''
    }

    out_errors = []

    validated = True
    try:
        deposit = context['deposit']
        if deposit.isnumeric():
            deposit = int(deposit)
        else:
            deposit = 0

        if deposit <= 0:
            print("deposit {}".format(deposit))
            errors['deposit'] = 'Please select deposit coin!'
            validated = False

        withdraw = context['withdraw']
        if withdraw.isnumeric():
            withdraw = int(withdraw)
        else:
            withdraw = 0

        if withdraw <= 0:
            errors['withdraw'] = 'Please select receive coin!'
            validated = False

        if context['rollback_wallet'].strip() == '':
            errors['rollback_wallet'] = 'Please add refund address!'
            validated = False

        for i in range(outs):
            address = context['dest_addr_{}'.format(i)]
            value = context['dest_amount_{}'.format(i)]
            if value.isnumeric():
                value = int(value)
            else:
                value = 0

            if address.strip() != '' and 0 <= value <= 100:
                total_sum = total_sum + value
            else:
                out_errors.append("Please input valid address and share.")
                validated = False

            # print('address {} value {} sum {}'.format(address, value, total_sum))

            if total_sum > 100:
                errors['over100'] = 'Sum of all addresses should be 100'
                validated = False
                break

        if total_sum < 100:
            errors['over100'] = 'Sum of all addresses should be 100'
            validated = False

        errors['outs'] = out_errors

        return errors, validated
    except Exception as ex:
        print(ex)
        return errors, False

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
                errors, validated = validate(context)
                if not validated:
                    context = request.POST.copy()
                    context['outs'] = outs
                    form = TransactionForm(context)
                    return render(request, 'exchange_form.html', {
                        'pairs': pairs,
                        'form': form,
                        'outs': range(0, outs),
                        'context': context,
                        'errors': errors
                    });

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
