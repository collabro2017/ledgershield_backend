from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url(r'coins', include('v1.coins.urls'))
]