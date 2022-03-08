from django.urls import path
from . import views

urlpatterns = [
    path('login', views.sellerLogin, name="sellerLogin"),
    path('register', views.sellerRegister, name="sellerRegister"),
    path('logout', views.sellerLogout, name="sellerLogout"),
    path('dashboard', views.sellerDashboard, name="sellerDashboard"),
    path('addproduct', views.addproduct, name="addproduct"),
    path('editProducts', views.editProducts, name="editProducts"),
    path('acceptOrder', views.acceptOrder, name="acceptOrder"),
    path('rejectOrder', views.rejectOrder, name="rejectOrder"),
    path('products', views.products, name="products"),
    path('account', views.editProfile, name="editProfile"),
    path('',views.sellerhome,name='sellerhome'),
    path('editstatus',views.editstatus,name='editstatus'),
    path('orderdetails/<id>',views.orderdetails,name='orderdetails'),

]
