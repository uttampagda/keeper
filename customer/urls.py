from django.urls import path
from . import views

urlpatterns = [
    path('', views.custDashboard, name='custhome'),
    path('login', views.custLogin, name="custLogin"),
    path('register', views.custRegister, name="custRegister"),
    path('addAddress', views.addAddress, name="addAddress"),
    path('logout', views.custLogout, name="custLogout"),
    path('dashboard', views.custDashboard, name="custDashboard"),
    path('searchProducts', views.searchProductNearBY, name="searchProductNearBY"),
    path('cart',views.cart,name='cart'),
    path('sellerlandingpage',views.sellerlandingpage,name='sellerlandingpage'),
    path('checkout', views.checkout, name = "checkout"),
    path('confirm', views.confirm, name = "confirm"),
    path('success', views.success, name="success"),
    path('banner', views.banner, name="banner"),
    path('orders', views.orders, name="orders"),
    path('profile', views.profile, name="profile"),
    path('dashboard', views.kmrange, name="kmrange"),
]
