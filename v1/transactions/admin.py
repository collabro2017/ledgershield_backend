from django.contrib import admin

from v1.transactions.models import Transaction, TransactionOutputs


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'order_id',
                    'date_created',
                    'deposit',
                    'withdraw',
                    'status',
                    'note')
    # readonly_fields = ('order_id',
    #                    'status',
    #                    'deposit',
    #                    'wallet_address',
    #                    'rollback_wallet',
    #                    'withdraw',
    #                    'withdrawl_address',
    #                    'exchange_rate',
    #                    'deposit_tx_hash',
    #                    'deposit_tx_amount',
    #                    'deposit_tx_confirmations'
    #                    )



admin.site.register(Transaction, TransactionAdmin)

class TransactionOutputAdmin(admin.ModelAdmin):
    list_display = ('address','value')

admin.site.register(TransactionOutputs, TransactionOutputAdmin)