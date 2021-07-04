from django.contrib import admin
from .models import Company, sharePrice, ShareCheckList, ShareWatchList

# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company', 'search_name','priceshortsearch', 'short_name', 'sector', 'sectorsearch','exchange')
    search_fields = ['company', 'search_name','priceshortsearch', 'short_name', 'sector', 'sectorsearch','exchange']
    ordering = ['company']
admin.site.register(Company,CompanyAdmin)

class sharePriceAdmin(admin.ModelAdmin):
    list_display = ('company_id_name', 'pricedate', 'openprice', 'closeprice')
    search_fields = ['company_id_name', 'pricedate', 'openprice', 'closeprice']
    ordering = ['pricedate']

    def company_id_name(self, obj):
        return obj.company_id.company


admin.site.register(sharePrice, sharePriceAdmin)


class shareCheckAdmin(admin.ModelAdmin):
    list_display = ('company_id_name', 'buyprice', 'buydate')
    search_fields = ['company_id_name', 'buyprice', 'buydate']
    ordering = ['buyprice']

    def company_id_name(self, obj):
        return obj.company_id.company

admin.site.register(ShareCheckList, shareCheckAdmin)


class shareWatchAdmin(admin.ModelAdmin):
    list_display = ('company_id_name', 'watchprice', 'watchdate')
    search_fields = ['company_id_name', 'watchprice', 'watchdate']
    ordering = ['watchprice']

    def company_id_name(self, obj):
        return obj.company_id.company

admin.site.register(ShareWatchList, shareWatchAdmin)

