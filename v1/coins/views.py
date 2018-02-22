
from rest_framework import generics
from rest_framework import permissions

from v1.coins.models import Coin
from v1.coins.serializers import CoinSerializer


class CoinListView(generics.ListAPIView):

    serializer_class = CoinSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Coin.objects.all()

    def get_queryset(self):
        return Coin.objects.filter(operational=True)