from django.urls import path
from . import views

urlpatterns = [
    path('login', views.custLogin, name="custLogin"),
    path('register', views.custRegister, name="custRegister"),
    path('logout', views.custLogout, name="custLogout"),
    path('dashboard', views.custDashboard, name="custDashboard"),
    path('',views.custhome,name='custhome'),
]
