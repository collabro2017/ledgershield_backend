from django.contrib import admin

from v1.transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','date_created','deposit', 'withdraw', 'status','note')


admin.site.register(Transaction, TransactionAdmin)