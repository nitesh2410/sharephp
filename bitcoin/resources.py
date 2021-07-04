from import_export import resources
from .models import Buy_sell_data

class CoinResources(resources.ModelResource):
    class meta:
        model = Buy_sell_data