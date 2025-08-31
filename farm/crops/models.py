from django.db import models
from django.contrib.auth.models import User
class Crops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True) 
    crop_image =models.ImageField(upload_to='static/')
    farmer_name = models.CharField(max_length=100)
    farmer_age = models.PositiveIntegerField()
    crop_name = models.CharField(max_length=100)
    crop_dryness = models.PositiveIntegerField()
    crop_bread = models.CharField(max_length=100)  
    crop_type = models.CharField(max_length=100)
    crop_description = models.TextField(null=True, blank=True)
    crop_quantity = models.PositiveIntegerField(help_text="In kg or appropriate unit")
    expected_price = models.PositiveIntegerField(help_text="In ₹ or appropriate currency")
    farming_location = models.CharField(max_length=255)
    croping_duration = models.CharField(max_length=100, help_text="e.g., 3 months, 90 days")

    def __str__(self):
        return f"{self.crop_name} by {self.farmer_name}"
