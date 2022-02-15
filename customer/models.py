from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Customer(models.Model):
    credentials = models.OneToOneField(User, related_name='Customer', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=250,unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cus_image = models.ImageField(upload_to='customer_image/'+str(username)+'/',default='default.jpg')
    access_review_to_seller_list = models.TextField(max_length=200, default="[]")

    def __str__(self):
        return self.username
    def save(self):
        for field in self._meta.fields:
            if field.name == 'cus_image':
                field.upload_to = 'cus_image/' + str(self.username) + '/'
        super(Customer, self).save()

class CustAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.PointField(srid=4326, geography=True, blank=True, null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=250)
    pincode = models.CharField(max_length=50)

class AllOrders(models.Model):
    customer_id = models.IntegerField(blank=False, null=False)
    customer_name = models.CharField(null=False, blank=False, default="NA", max_length=100)
    seller_id = models.IntegerField(blank=False, null=False)
    payment_id = models.CharField(blank=False, null=False, max_length=120)
    payment_created_at = models.CharField(blank=True, null=True, max_length=120)
    amount_paid = models.FloatField(blank=True, null=True)
    ttl_amount = models.FloatField(blank=True, null=True)
    amount_due = models.FloatField(blank=True, null=True)
    order_details = models.CharField(blank=False, null=False, max_length=1000)
    is_accepted = models.BooleanField(default=None, blank=True, null=True)
    is_delivered = models.BooleanField(default=None, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_rejected = models.BooleanField(default=None, blank=True, null=True)
    order_type = models.CharField(blank=False, null=False, max_length=50, default="HOME_DELIVERY")
    order_status = models.CharField(blank=False, null=False, max_length=50, default="PENDING")
    pickup_date = models.DateTimeField(blank=True, null=True)


class Banner(models.Model):
    banner_title=models.CharField(max_length=50)
    banner_photo = models.ImageField(upload_to="banner/")
    prio = models.IntegerField(blank=False,null=False,unique=True)


    def __str__(self):
        return self.banner_title
