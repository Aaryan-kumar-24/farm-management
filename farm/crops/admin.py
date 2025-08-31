from django.contrib import admin

from .models import Crops

class CropsAdmin(admin.ModelAdmin):
    list_display = ('crop_image',
        'farmer_name',
'farmer_age',
'crop_name',
'crop_dryness',
'crop_bread',
'crop_type',
'crop_description',
'crop_quantity',
'expected_price',
'farming_location',
'croping_duration')
    
admin.site.register(Crops,CropsAdmin)
