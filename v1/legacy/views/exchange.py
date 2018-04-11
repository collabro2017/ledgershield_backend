from django.shortcuts import render
from v1.coins.models import CoinPair, Coin

def index(request, deposit):
    symbol = deposit.upper()
    pairs = CoinPair.objects.filter(source__symbol=symbol)
    coins = Coin.objects.all()
    return render(request, 'exchange_form.html', {
        'coins': coins,
        'pairs': pairs
    });