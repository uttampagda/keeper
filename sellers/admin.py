from django.contrib import admin
from sellers.models import Seller, AllCategories, Product

admin.site.register(Seller)
admin.site.register(AllCategories)
admin.site.register(Product)