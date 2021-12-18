from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from customer.models import Customer, CustAddress,Banner
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from sellers.models import Seller,Product
def home(request):
    bannerr = Banner.objects.all()
    print(bannerr)
    data = {
        'bannerr': bannerr,
    }
    return render(request, 'home.html',data)
