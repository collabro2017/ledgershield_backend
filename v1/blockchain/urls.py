from django.conf.urls import url
from v1.blockchain.views.bitcoin import BitcoinStealthAddress

urlpatterns = [
    url(r'^bitcoin/(?P<src>[0-9A-Za-z_-]+)/(?P<dst>[0-9A-Za-z_-]+)$', BitcoinStealthAddress.as_view(), name="bitcoin-stealth-address")
]