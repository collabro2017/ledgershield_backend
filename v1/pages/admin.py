from django.contrib import admin

from v1.pages.models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug')
    readonly_fields = ('slug',)

admin.site.register(Page, PageAdmin)