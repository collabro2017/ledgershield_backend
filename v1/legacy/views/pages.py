from django.shortcuts import render
from v1.coins.models import Coin

def index(request):

    coins = Coin.objects.all()

    return render(request, 'home.html', {
        'coins': coins
    })


def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def serice_fee(request):
    return render(request, 'service_fee.html')

def contact_us(request):
    return render(request, 'contact_us.html')