from django.contrib.auth.models import User
from django.db import models

class Seller(models.Model):
    credentials = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE)

    email = models.CharField(max_length=250,unique=True)
    username = models.CharField(max_length=50, unique=True)
    shopname = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    lat = models.DecimalField(max_digits=19, decimal_places=16)
    lon = models.DecimalField(max_digits=19, decimal_places=16)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    product_name = models.CharField(max_length=300)
    price = models.IntegerField()
    seller_cr = models.IntegerField()
    is_featured = models.BooleanField(default=False)
    #product_image = models.ImageField(upload_to='media/seller/')

