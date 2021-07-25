from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    credentials = models.OneToOneField(User, related_name='Customer', on_delete=models.CASCADE)

    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=250,unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)