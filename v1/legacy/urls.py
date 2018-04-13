from django.conf.urls import url
from .views import home, exchange, transaction

urlpatterns = [
    url(r'exchange/(?P<deposit>[^\/]+)$', exchange.index ),
    url(r'tx/status/(?P<order_id>[^\/]+)$', transaction.index),
    url(r'^$', home.index)

]