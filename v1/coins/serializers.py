from rest_framework import serializers

from v1.coins.models import Coin, CoinPair


class CoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coin
        fields = ('id','name','symbol','image', 'operational','block_explorer_url')


class CoinPairSerializer(serializers.ModelSerializer):
    source = CoinSerializer(many=False)
    destination = CoinSerializer(many=False)

    class Meta:
        model = CoinPair
        fields = ('id', 'source', 'destination', 'rate', 'minerFee')