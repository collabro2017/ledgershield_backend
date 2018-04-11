from django.shortcuts import render
from v1.coins.models import Coin

def index(request):

    coins = Coin.objects.all()

    return render(request, 'home.html', {
        'coins': coins
    })