from rest_framework import serializers
from v1.transactions.models import Transaction
from v1.coins.serializers import  CoinSerializer


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id',
                  'order_id',
                  'status',
                  'deposit',
                  'wallet_address',
                  'deposit_tx_hash',
                  'deposit_tx_amount',
                  'rollback_wallet',
                  'withdraw',
                  'withdrawl_address',
                  'note')
        read_only_fields = ('wallet_address', 'order_id','deposit_tx_hash','deposit_tx_amount')

class TransactionDetailSerializer(serializers.ModelSerializer):
    deposit = CoinSerializer(read_only=True)
    withdraw = CoinSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id',
                  'order_id',
                  'status',
                  'deposit',
                  'wallet_address',
                  'deposit_tx_hash',
                  'deposit_tx_amount',
                  'deposit_tx_confirmations',
                  'rollback_wallet',
                  'withdraw',
                  'withdrawl_address',
                  'note')
        read_only_fields = ('wallet_address', 'order_id','deposit_tx_hash','deposit_tx_amount','deposit_tx_confirmations')
