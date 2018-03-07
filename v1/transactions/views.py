from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets, generics, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from v1.blockchain.lib.bitcoin import Bitcoin
from v1.transactions.models import Transaction
from v1.transactions.serializers import TransactionSerializer, TransactionDetailSerializer
from v1.transactions.tasks import getExchangeRate

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (AllowAny,)


class TransactionByOrderIDView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'order_id'

class TestTask(views.APIView):

    def get(self, request, *args, **kwargs):
        txid = kwargs['txid'];
        tx = Transaction.objects.get(pk=txid)
        # wait_for_deposit.delay(txid)

        # d.append(Bitcoin().getWallet())
        # st, data = Bitcoin().getTxByHash(tx.deposit_tx_hash)
        # d = data
        st, data = Bitcoin().getWalletTxDetail(tx.deposit_tx_hash)
        # st, data = Bitcoin().getTxOut([tx.deposit_tx_hash, tx.deposit_tx_index])
        # get_deposit_address.delay(txid)
        getExchangeRate.delay(txid)
        # channel_name = 'txchannel-{}'.format(tx.order_id)
        # chanel_layer = get_channel_layer()
        # async_to_sync(chanel_layer.group_send)(channel_name, {
        #     'type': 'update.txinfo',
        #     'text': txid
        # })
        return Response({'data': data}, status=status.HTTP_200_OK)