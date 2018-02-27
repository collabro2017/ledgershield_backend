from rest_framework import serializers

class BitcoinSerializers(serializers.Serializer):
    """ Bitcoin Stealth Address Serializer """
    address = serializers.CharField(max_length=100)
    account = serializers.CharField(max_length=50)
