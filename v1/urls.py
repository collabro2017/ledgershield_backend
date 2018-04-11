from django.conf.urls import url
from django.urls import include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Ledger Shield API')

urlpatterns = [
    url(r'coins/', include('v1.coins.urls')),
    url(r'wallet/', include('v1.blockchain.urls')),
    url(r'transactions/', include('v1.transactions.urls')),
    url(r'^$', schema_view)
]
