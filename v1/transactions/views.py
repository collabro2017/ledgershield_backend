from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from v1.transactions.models import Transaction
from v1.transactions.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (AllowAny,)