from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Customer(models.Model):
    credentials = models.OneToOneField(User, related_name='Customer', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=250,unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CustAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.PointField(srid=4326, geography=True, blank=True, null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=250)
    pincode = models.CharField(max_length=50)

class AllOrders(models.Model):
    customer_id = models.IntegerField(blank=False, null=False)
    seller_id = models.IntegerField(blank=False, null=False)
    payment_id = models.CharField(blank=False, null=False, max_length=120)
    payment_created_at = models.CharField(blank=True, null=True, max_length=120)
    amount_paid = models.FloatField(blank=True, null=True)
    ttl_amount = models.FloatField(blank=True, null=True)
    amount_due = models.FloatField(blank=True, null=True)
    order_details = models.CharField(blank=False, null=False, max_length=1000)
    is_accepted = models.BooleanField(default=None)
    is_delivered = models.BooleanField(default=None)
    created_date = models.DateTimeField(auto_now=True)
    is_rejected = models.BooleanField(default=None)
