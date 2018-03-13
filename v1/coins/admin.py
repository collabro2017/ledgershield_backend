from django.contrib import admin

# Register your models here.
from v1.coins.models import Coin, CoinPair


class CoinAdmin(admin.ModelAdmin):
    list_display = ('name','symbol','service_fee','operational', 'decimals' ,'date_modified')


class CoinPairAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'dst_rate', 'date_modified')
    readonly_fields = ('dst_rate',)

    def dst_rate(self, obj):
        return '{} {}'.format(obj.rate, obj.destination.symbol)

    dst_rate.short_description = 'Rate'


admin.site.register(Coin, CoinAdmin)
admin.site.register(CoinPair, CoinPairAdmin)