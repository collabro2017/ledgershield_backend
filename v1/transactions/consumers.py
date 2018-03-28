from channels.generic.websocket import AsyncJsonWebsocketConsumer
from v1.transactions.models import Transaction
from django.core import serializers

from v1.transactions.serializers import TransactionDetailSerializer


class TransactionConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.txid = self.scope['url_route']['kwargs']['txid']
        await self.channel_layer.group_add('txchannel-{}'.format(self.txid),self.channel_name)


    async def receive(self, text_data=None, bytes_data=None):
        tx = Transaction.objects.filter(order_id=self.txid)
        t = serializers.serialize('json', tx)
        await self.send_json(t)

    async def disconnect(self, code):
        await self.channel_layer.group_discard('txchannel', self.channel_name)

    async def update_txinfo(self, event):
        print(event)
        tx = Transaction.objects.get(pk=event['text'])
        t = TransactionDetailSerializer(tx)

        await self.send_json(t.data)