from django.conf.urls import url
from django.urls import include



urlpatterns = [
    url(r'coins', include('v1.coins.urls')),
    url(r'wallet/', include('v1.blockchain.urls')),
    url(r'transactions/', include('v1.transactions.urls'))
]