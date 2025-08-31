from django.contrib import admin

from .models import Buyier

class BuyierAdmin(admin.ModelAdmin):
    list_display = ('buyer_name',
'buyer_address',
'purchase_quantity',
'negotiation_price',
    'crop_name',
    'farmer_name',
    'buyer_phone',
)
    
admin.site.register(Buyier,BuyierAdmin)
