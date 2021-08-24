from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Customer, CustAddress
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from sellers.models import Seller,Product
from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

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
    km_range = 10

    try:
        allAddress = CustAddress.objects.filter(customer=customer_data)
        ref_location = allAddress[0].location

        if request.method == "POST":
            km_range = request.POST['km_range']

        NearBySellers = Seller.objects.filter(location__dwithin=(ref_location, D(km=km_range)))
        print(NearBySellers)
        for seller in NearBySellers:
            print(seller.username)

        return render(request, 'customer/dashboard.html',
                      {'customer_data': customer_data, 'near_by_sellers': NearBySellers})
    except:
        NearBySellers = {}
        messages.error(request, 'Please add Address first!')
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
        lon = latiLong[1]
        customer = Customer.objects.get(username=request.user.username)

        try:
            CustAddress(
                customer=customer,
                address=address,
                city=city,
                pincode=pincode,
                location = Point(float(lon), float(lat), srid=4326)
            ).save()
            messages.success(request, 'Address added successfully')
            return redirect('custDashboard')
        except Exception as er:
            messages.error(request, er)
            return render(request, 'customer/addAddress.html')
    else:
        return render(request, 'customer/addAddress.html')

def sellerlandingpage(request):
    if request.method == "GET":
        print(request.GET["seller_name"])
        seller_detail = Seller.objects.get(username=request.GET["seller_name"])
        seller_products = Product.objects.filter(seller_cr=seller_detail.id)

        data ={
          'products': seller_products,
        }
    return render(request, 'customer/sellerlandingpage.html',data)


