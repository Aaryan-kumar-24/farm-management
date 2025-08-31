from django.db import models
from django.contrib.auth.models import User
class Chat(models.Model):
    chat= models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

