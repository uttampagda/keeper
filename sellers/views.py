from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Seller,Product
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from customer.models import AllOrders
import datetime

# Create your views here.

def sellerRegister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        shopname = request.POST['shopname']
        email = request.POST['email']
        phone = request.POST['phone']
        latiLong = request.POST['latiLong'].split(',')
        #TODO VALIDATION ON latLong check valid or not
        lat = latiLong[0]
        log = latiLong[1]
        password = request.POST['password']

        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if Seller.objects.filter(username=username).exists():
                messages.warning(request, 'Username exists')
                return redirect('sellerRegister')
            else:
                if Seller.objects.filter(email=email).exists():
                    messages.warning(request, 'email already exists')
                    return redirect('sellerhome')
                else:
                    credentials = User.objects.create_user(
                        username=username,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )

                    user = Seller(
                        credentials=credentials,
                        shopname=shopname,
                        username=username,
                        email=email,
                        phone=phone,
                        location = Point(float(log), float(lat), srid=4326)
                    )
                    user.save()
                    messages.success(request, 'Account created successfully')
                    return redirect('sellerDashboard')
        else:
            messages.warning(request, 'Password do not match')
            return redirect('sellerRegister')

    return render(request, 'seller/register.html')

def sellerLogin(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if Seller.objects.filter(username=username).exists():
                    auth.login(request, user)
                    messages.warning(request, 'you are logged in')
                    return redirect('sellerDashboard')
                else:
                    messages.warning(request, 'You are not seller')
                    return redirect('sellerLogin')
            else:
                messages.warning(request, 'invalid credentials')
                return redirect('sellerLogin')

        return render(request, 'seller/login.html')

@login_required(login_url='sellerLogin')
def sellerDashboard(request):
    if request.user.is_authenticated:
        seller_data = Seller.objects.get(credentials_id = request.user.id)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=5)
        new_orders = AllOrders.objects.filter(seller_id = request.user.id, created_date__range=(earlier, now)).exclude(is_accepted = True)
        accepted_orders = AllOrders.objects.filter(seller_id = request.user.id, is_accepted = True)
        print(new_orders, accepted_orders)
        return render(request, 'seller/dashboard.html', {'seller_data':seller_data, 'new_orders': new_orders, 'accepted_orders': accepted_orders})
    else:
        redirect('sellerLogin')

def sellerLogout(request):
    logout(request)
    return redirect('sellerhome')

def sellerhome(request):
    return render(request,'seller/home.html')

@login_required(login_url='sellerLogin')
def addproduct(request):
    print(request.user.id)
    if request.method == 'POST':
      product_name = request.POST['product_name']
      price = request.POST['price']
      #product_image = request.POST['username']

      seller_cr = request.user.id
      addproduct = Product(seller_cr=seller_cr,product_name=product_name,price=price)

      addproduct.save()
      print('saved')
      return redirect('sellerDashboard')
    return render(request, 'seller/addproduct.html')

@login_required(login_url='sellerLogin')
def acceptOrder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            order_id = request.POST['order_id']
            acceptOrd = AllOrders.objects.get(id = order_id)
            acceptOrd.is_accepted = True
            acceptOrd.save()

        seller_data = Seller.objects.get(credentials_id = request.user.id)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=5)
        new_orders = AllOrders.objects.filter(seller_id = request.user.id, created_date__range=(earlier, now)).exclude(is_accepted = True)
        accepted_orders = AllOrders.objects.filter(seller_id = request.user.id, is_accepted = True)
        print(new_orders, accepted_orders)
        return render(request, 'seller/dashboard.html', {'seller_data':seller_data, 'new_orders': new_orders, 'accepted_orders': accepted_orders})
    else:
        redirect('sellerLogin')


@login_required(login_url='sellerLogin')
def products(request):
    products = Product.objects.all()

    data = {
        'products' : products
    }
    return render(request, 'seller/products.html', data)

