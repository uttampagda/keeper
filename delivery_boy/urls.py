from django.urls import path
from . import views

urlpatterns = [
    path('login', views.deliboyLogin, name="deliboyLogin"),
    path('register', views.deliboyRegister, name="deliboyRegister"),
    path('logout', views.deliboyLogout, name="deliboyLogout"),
    path('dashboard', views.deliboyDashboard, name="deliboyDashboard"),
    path('',views.deliboyhome,name='deliboyhome'),
]
