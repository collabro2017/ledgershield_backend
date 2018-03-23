
from rest_framework import generics, status, views
from rest_framework import permissions
from rest_framework.response import Response

from v1.coins.models import Coin, CoinPair
from v1.coins.serializers import CoinSerializer, CoinPairSerializer


class CoinListView(generics.ListAPIView):

    serializer_class = CoinSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Coin.objects.all()

    # def get_queryset(self):
    #     return Coin.objects.filter(operational=True)

class CoinListViewBySource(generics.ListAPIView):

    serializer_class = CoinPairSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = CoinPair.objects.all()
    # lookup_field = 'symbol'

    def get_queryset(self):
        symbol = self.kwargs.get('symbol')
        return CoinPair.objects.filter(source__symbol=symbol)