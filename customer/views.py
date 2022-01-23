from datetime import datetime

from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Customer, CustAddress, AllOrders, Banner
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from sellers.models import Seller, Product, AllCategories
from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.shortcuts import render
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt


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
    km_range = 10000

    allcategories = AllCategories.objects.all()

    try:
        allAddress = CustAddress.objects.filter(customer=customer_data)
        ref_location = allAddress[0].location

        if request.method == "POST":
            km_range = request.POST.get('km_range')
            category_name = request.POST.get('category_name')
            product_name = request.POST.get('product_name')



            if km_range is None or km_range == '':
                km_range = 10000

            if category_name is not None:
                NearBySellers = Seller.objects.filter(location__dwithin=(ref_location, D(km=km_range)), categories_list__contains=category_name)
            if product_name is not None:
                NearBySellers = Product.objects.filter(
                    location__dwithin=(ref_location, D(km=km_range)),
                    product_name__startswith=product_name)


            return render(request, 'customer/dashboard.html',
                          {'customer_data': customer_data, 'near_by_sellers': NearBySellers,
                           'allcategories': allcategories})

        NearBySellers = Seller.objects.filter(location__dwithin=(ref_location, D(km=km_range)))


        return render(request, 'customer/dashboard.html',
                      {'customer_data': customer_data, 'near_by_sellers': NearBySellers, 'allcategories':allcategories})
    except:
        NearBySellers = {}
        messages.error(request, 'Please add Address first!')
        return render(request, 'customer/dashboard.html',
                      {'customer_data': customer_data, 'near_by_sellers': NearBySellers})


@login_required(login_url='custLogin')
def searchProductNearBY(request):
    customer_data = Customer.objects.get(username=request.user.username)
    km_range = 10

    try:
        allAddress = CustAddress.objects.filter(customer=customer_data)
        ref_location = allAddress[0].location

        if request.method == "POST":
            km_range = request.POST.get('km_range')
            key_word = request.POST['key_word']

            if km_range is None or km_range == '':
                km_range = 10

            if key_word is None or key_word == '':
                NearBySellers = Seller.objects.filter(location__dwithin=(ref_location, D(km=10)))
                messages.error(request, 'Please search valid keyword')
                return render(request, 'customer/dashboard.html',
                              {'customer_data': customer_data, 'near_by_sellers': NearBySellers})

        NearByProduct = Product.objects.filter(location__dwithin=(ref_location, D(km=km_range)),
                                               product_name__icontains=key_word)



        return render(request, 'customer/productSearch.html', {'product_data': NearByProduct})
    except Exception as er:
        NearBySellers = {}
        messages.error(request, 'Please add Address first!')
        return render(request, 'customer/dashboard.html',
                      {'customer_data': customer_data, 'near_by_sellers': NearBySellers})


def custLogout(request):
    logout(request)
    return redirect('custhome')


@login_required(login_url='custLogin')
def custhome(request):
    return redirect('custDashboard')


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
                location=Point(float(lon), float(lat), srid=4326)
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
        seller_detail = Seller.objects.get(username=request.GET["seller_name"])
        seller_products = Product.objects.filter(seller_cr=seller_detail.credentials_id,is_featured=True)
        loc=seller_detail.location
        seller_id = seller_detail.credentials_id
        customer = Customer.objects.get(username=request.user.username)
        data = {
            'products': seller_products,
            'customer': customer,
            'seller_id': seller_id,
            'seller_detail': seller_detail,
            'loc': loc,
        }
    return render(request, 'customer/sellerlandingpage.html', data)


def cart(request):
    return render(request, 'customer/cart.html')


def confirm(request):
    if request.method == "POST":
        name = request.POST.get('name')
        list_of_orders = request.POST.get('product_list')
        order_type = request.POST.get('order_type')
        pick_up_time = request.POST.get('pick_up_time')
        total = request.POST.get('total')
        amount = int(total)
        return render(request, 'customer/checkout.html',
                      {'list_of_orders': list_of_orders, 'name': name, 'total': int(total), 'amount': int(amount),
                       'order_type': order_type, 'pick_up_time': pick_up_time})
    else:
        return render(request, 'customer/cart.html')


def checkout(request):
    if request.method == "POST":
        order_type = request.POST.get('order_type')
        pick_up_date = request.POST.get('pick_up_date')

        if pick_up_date == '':
            pick_up_date = None

        amount = request.POST.get('total').replace('/', '')
        list_of_orders = request.POST.get('list_of_orders').replace('/', '')

        client = razorpay.Client(auth=("rzp_test_bSTKVqtv6GwTso", "YEAj0ll32SLlXhunbTJSJqVH"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        customer_data = Customer.objects.get(username=request.user.username)

        seller_id = Product.objects.get(pk=json.loads(list_of_orders)[0]['proid']).seller_cr

        new_order = AllOrders(
            customer_id=customer_data.credentials_id,
            customer_name=request.user.username,
            seller_id=seller_id,
            payment_id=payment['id'],
            ttl_amount=amount,
            amount_paid=payment['amount_paid'],
            amount_due=payment['amount_due'],
            order_details=list_of_orders,
            payment_created_at=payment['created_at'],
            is_delivered=False,
            is_accepted=False,
            is_rejected=False,
            order_type=order_type,
            pickup_date=pick_up_date
        )
        new_order.save()
        return render(request, "customer/success.html")
    else:
        return render(request, 'customer/cart.html')


@csrf_exempt
def success(request):
    return render(request, "customer/success.html")


def banner(request):
    bannerr = Banner.objects.all()
    data = {
        'bannerr': bannerr,
    }
    return render(request, "customer/dashboard.html", data)


def orders(request):
    order_data = AllOrders.objects.all().filter(customer_id=request.user.id)
    data = {
        'order_data': order_data,
    }

    return render(request, "customer/myorderview.html", data)

@login_required(login_url='cusLogin')
def profile(request):
    if request.method == 'GET':
        customer_data = Customer.objects.get(credentials_id=request.user.id)
        profile_to_be_edit = Customer.objects.get(credentials_id=request.user.id)
        return render(request, 'customer/profileview.html', {'profile_to_be_edit': profile_to_be_edit, 'customer_data': customer_data})

    if request.method == 'POST':
        profile_to_be_edit = Customer.objects.get(credentials_id=request.user.id)
        user_to_be_edit = User.objects.get(id=request.user.id)

        newpassword = request.POST.get('newpassword')
        newconfirmpassword = request.POST.get('newconfirmpassword')
        if newpassword != "" and newconfirmpassword != "" and newpassword == newconfirmpassword:
            u = User.objects.get(id=request.user.id)
            u.set_password(newpassword)
            u.save()
            print("password updated")

        user_to_be_edit.first_name = request.POST.get('first_name')
        profile_to_be_edit.phone = request.POST.get('phone')

        profile_to_be_edit.save()
        user_to_be_edit.save()
        return redirect('custDashboard')
