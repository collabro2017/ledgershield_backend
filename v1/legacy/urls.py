from django.conf.urls import url
from .views import home, exchange

urlpatterns = [
    url(r'exchange/(?P<deposit>[^\/]+)$', exchange.index ),
    url(r'^$', home.index)

]