from django.conf.urls import url
from rest_framework import routers
from .views import CoinListView, CoinListViewBySource

urlpatterns = [
    url(r'list/(?P<symbol>[^\/]+)$', CoinListViewBySource.as_view(), name='coin_list_bysource'),
    url(r'list/', CoinListView.as_view(), name="coin_list")
]