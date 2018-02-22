from rest_framework import serializers

from v1.coins.models import Coin


class CoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coin
        fields = ('id','name','symbol','image')
