from django.contrib import admin

# Register your models here.
from v1.coins.models import Coin


class CoinAdmin(admin.ModelAdmin):
    list_display = ('name','symbol','operational')


admin.site.register(Coin, CoinAdmin)