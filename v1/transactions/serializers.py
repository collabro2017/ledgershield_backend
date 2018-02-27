from rest_framework import serializers
from v1.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'wallet_address', 'rollback_wallet', 'withdrawl_address', 'deposit_tx_hash', 'status', 'note', 'deposit', 'withdraw')
        read_only_fields = ('wallet_address',)