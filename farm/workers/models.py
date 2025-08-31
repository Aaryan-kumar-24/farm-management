from django.db import models
from django.contrib.auth.models import User
class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    worker_name = models.CharField(max_length=100)
    worker_age = models.PositiveIntegerField()
    working_job = models.CharField(max_length=100)
    working_duration = models.PositiveIntegerField()
    worker_phone = models.CharField(max_length=15)
    worker_payment = models.PositiveIntegerField()  # Using int instead of decimal
    worker_address = models.CharField(max_length=255)
    worker_image = models.ImageField(upload_to='static/')

    def __str__(self):
        return self.worker_name
