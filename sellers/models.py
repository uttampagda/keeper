from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    credentials = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE)

    email = models.CharField(max_length=250,unique=True)
    username = models.CharField(max_length=50, unique=True)
    shopname = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    price = models.IntegerField(max_length=100)
