from rest_framework import views
from rest_framework.response import Response

from v1.blockchain.serializers import blockchain
from v1.blockchain.utils import Utils

class BitcoinStealthAddress(views.APIView):

    def get(self, request, src, dst):
        accountName = Utils.getAccountName(src, dst)
        name, address =  Utils.getDespositAddress(src, accountName)
        serializer = blockchain.BitcoinSerializers({'address':address, 'account':name})
        return Response(serializer.data)