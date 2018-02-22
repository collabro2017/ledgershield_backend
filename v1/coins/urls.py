from django.conf.urls import url
from rest_framework import routers
from .views import CoinListView

urlpatterns = [
    url(r'list/', CoinListView.as_view(), name="coin_list")
]