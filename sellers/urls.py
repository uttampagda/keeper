from django.urls import path
from . import views

urlpatterns = [
    path('login', views.sellerLogin, name="sellerLogin"),
    path('register', views.sellerRegister, name="sellerRegister"),
    path('logout', views.sellerLogout, name="sellerLogout"),
    path('dashboard', views.sellerDashboard, name="sellerDashboard"),
    path('addproduct', views.addproduct, name="addproduct"),
    path('acceptOrder', views.acceptOrder, name="acceptOrder"),
    path('rejectOrder', views.rejectOrder, name="rejectOrder"),
    path('products', views.products, name="products"),

    path('',views.sellerhome,name='sellerhome'),
]
