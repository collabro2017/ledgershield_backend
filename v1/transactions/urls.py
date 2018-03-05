from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from .views import TransactionViewSet, TransactionByOrderIDView, TestTask


transaction_routers = routers.DefaultRouter()
transaction_routers.register(r'', TransactionViewSet, base_name='transactions')

urlpatterns = [
    url(r'^detail/(?P<order_id>[^\/]+)$', TransactionByOrderIDView.as_view(), name='tx_by_order_id'),
    url(r'^test/(?P<txid>[^\/]+)$', TestTask.as_view(), name='test-task' ),
    url(r'^', include(transaction_routers.urls))
]