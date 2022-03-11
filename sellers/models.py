from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Seller(models.Model):
    credentials = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE)
    email = models.CharField(max_length=250,unique=True)
    username = models.CharField(max_length=50, unique=True)
    shopname = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    location = models.PointField(srid=4326, geography=True, blank=True, null=True)
    categories_list = models.TextField(max_length=200, default="[]")
    created_at = models.DateTimeField(auto_now_add=True)
    shop_image = models.ImageField(upload_to='sellers_image/'+str(username)+'/',default='default.jpg')

    total_stars = models.IntegerField(default=0)
    total_reviews = models.IntegerField(default=0)
    avarage_review = models.FloatField(default=0.0)
    def __str__(self):
        return self.shopname
    def save(self):
        for field in self._meta.fields:
            if field.name == 'shop_image':
                field.upload_to = 'sellers_image/' + self.shopname + '/'
        super(Seller, self).save()

class Product(models.Model):
    product_name = models.CharField(max_length=300)
    product_disc = models.CharField(max_length=500)
    price = models.IntegerField()
    seller_cr = models.IntegerField()
    is_featured = models.BooleanField(default=False)
    shopname = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='products/sellers/')
    location = models.PointField(srid=4326, geography=True, blank=True, null=True)
    product_category = models.CharField(max_length=100, blank=False, null=False)

    def save(self):
        for field in self._meta.fields:
            if field.name == 'product_image':
                field.upload_to = 'AllProducts/sellers/{}/{}/'.format(self.shopname, self.product_name)
        super(Product, self).save()

    def __str__(self):
        return self.product_name


class AllCategories(models.Model):
    category_name = models.CharField(max_length=100)
    category_img= models.ImageField(upload_to='cat_image/',default='default.jpg')
    def __str__(self):
        return self.category_name
