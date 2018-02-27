from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from .views import TransactionViewSet


transaction_routers = routers.DefaultRouter()
transaction_routers.register(r'', TransactionViewSet, base_name='transactions')

urlpatterns = [
    url(r'^', include(transaction_routers.urls))
]