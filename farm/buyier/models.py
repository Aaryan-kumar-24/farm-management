from django.db import models
from django.contrib.auth.models import User
class Buyier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    buyer_name =models.CharField(max_length=100)
    buyer_address =models.CharField(max_length=100)
    purchase_quantity = models.PositiveIntegerField()
    negotiation_price = models.PositiveIntegerField()
    farmer_name = models.CharField(max_length=100, default='Unknown')  # <-- Added default
    crop_name = models.CharField(max_length=100, default='Unknown')    
    buyer_phone= models.PositiveIntegerField()

    def __str__(self):
        return f"{self.buyer_name} -> {self.crop_name}"

