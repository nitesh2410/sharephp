from django.contrib import admin
from .models  import Buy_sell_data, coin_average
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class importAdmin(ImportExportModelAdmin):
    list_display = ('datadate', 'coin', 'price', 'volume', 'amount', 'trade')
    search_fields = ['coin', 'trade']

admin.site.register(Buy_sell_data, importAdmin)


class CoinAverageAdmin(admin.ModelAdmin):
    list_display = ('coin', 'volume','amount','average','TotalProfit')
    search_fields = ['coin']
    ordering = ['coin']

admin.site.register(coin_average,CoinAverageAdmin)