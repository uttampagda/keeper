from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Customer, CustAddress
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db import models
from sellers.models import Seller

# Create your views here.

def custRegister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']

        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if Customer.objects.filter(username=username).exists():
                messages.warning(request, 'Username exists')
                return redirect('custRegister')
            else:
                if Customer.objects.filter(email=email).exists():
                    messages.warning(request, 'email already exists')
                    return redirect('custhome')
                else:
                    credentials = User.objects.create_user(
                        username=username,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )

                    user = Customer(
                        credentials=credentials,
                        username=username,
                        email=email,
                        phone=phone,
                    )
                    user.save()
                    messages.success(request, 'Account created successfully')
                    return redirect('custDashboard')
        else:
            messages.warning(request, 'Password do not match')
            return redirect('custRegister')

    return render(request, 'customer/register.html')

def custLogin(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if Customer.objects.filter(username=username).exists():
                    auth.login(request, user)
                    messages.warning(request, 'you are logged in')
                    return redirect('custDashboard')
                else:
                    messages.warning(request, 'you are not customer')
                    return redirect('custLogin')
            else:
                messages.warning(request, 'invalid credentials')
                return redirect('custLogin')
        return render(request, 'customer/login.html')

@login_required(login_url='custLogin')
def custDashboard(request):
    customer_data = Customer.objects.get(username=request.user.username)
    allAddress = CustAddress.objects.filter(customer=customer_data)
    latitude = allAddress[0].lat
    longitude = allAddress[1].log

    radius_km = request.data.get('radius', 10)
    queryset = Seller.objects.annotate(
        radius_sqr=pow(models.F('loc__latitude') - latitude, 2) + pow(models.F('loc__longitude') - longitude, 2)
    ).filter(
        radius_sqr__lte=pow(radius_km / 9, 2)
    )
    NearBySellers = dict(location=queryset)

    print(NearBySellers)
    for seller in NearBySellers:
        print(seller.username)
    return render(request, 'customer/dashboard.html', {'customer_data': customer_data, 'near_by_sellers': NearBySellers})

def custLogout(request):
    logout(request)
    return redirect('custhome')

@login_required(login_url='custLogin')
def custhome(request):
    return render(request,'customer/home.html')

@login_required(login_url='custLogin')
def addAddress(request):
    if request.method == "POST":
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        latiLong = request.POST['latiLong'].split(',')
        lat = latiLong[0]
        log = latiLong[1]
        customer = Customer.objects.get(username=request.user.username)

        try:
            CustAddress(
                customer=customer,
                address=address,
                city=city,
                pincode=pincode,
                lat=lat,
                log=log
            ).save()
            messages.success(request, 'Address added successfully')
            return redirect('custDashboard')
        except Exception as er:
            messages.error(request, er)
            return render(request, 'customer/addAddress.html')
    else:
        return render(request, 'customer/addAddress.html')