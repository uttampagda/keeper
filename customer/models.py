from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    credentials = models.OneToOneField(User, related_name='Customer', on_delete=models.CASCADE)

    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=250,unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CustAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=19, decimal_places=16)
    lon = models.DecimalField(max_digits=19, decimal_places=16)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=250)
    pincode = models.CharField(max_length=50)