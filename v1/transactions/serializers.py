from rest_framework import serializers
from v1.transactions.models import Transaction, TransactionOutputs
from v1.coins.serializers import  CoinSerializer


class TransactionOutputsSerializer(serializers.ModelSerializer):

    class Meta:
        model= TransactionOutputs
        fields = ('address', 'value', 'tx_hash')


class TransactionSerializer(serializers.ModelSerializer):

    outs =  TransactionOutputsSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ('id','order_id','status','deposit','wallet_address', 'deposit_tx_hash',
                  'deposit_tx_amount','rollback_wallet', 'withdraw', 'exchange_rate', 'note', 'outs'
                )
        read_only_fields = ('wallet_address', 'order_id','deposit_tx_hash','deposit_tx_amount','exchange_rate')

    def create(self, validated_data):
        outs = validated_data.pop('outs')
        tx = Transaction.objects.create(**validated_data)
        tx_outputs = []
        for output in outs:
            tx_ouput = TransactionOutputs.objects.create(**output)
            tx_outputs.append(tx_ouput.pk)

        tx.outs.set(tx_outputs)
        tx.save()
        return tx



class TransactionDetailSerializer(serializers.ModelSerializer):
    deposit = CoinSerializer(read_only=True)
    withdraw = CoinSerializer(read_only=True)
    outs = TransactionOutputsSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'order_id', 'status', 'deposit', 'wallet_address', 'deposit_tx_hash', 'date_modified', 'date_created',
                  'deposit_tx_amount', 'deposit_tx_confirmations', 'rollback_wallet', 'withdraw', 'exchange_rate', 'note', 'outs'
                  )
        read_only_fields = ('wallet_address', 'order_id', 'deposit_tx_hash', 'deposit_tx_amount', 'deposit_tx_confirmations',
                            'exchange_rate', 'date_modified', 'date_created')
