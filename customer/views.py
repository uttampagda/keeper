from datetime import datetime

from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

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
from geopy.distance import geodesic


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
                return redirect('custDashboard')
            else:
                messages.warning(request, 'you are not customer')
                return redirect('custLogin')
        else:
            messages.warning(request, 'Please enter valid details!')
            return redirect('custLogin')
    return render(request, 'customer/login.html')


def kmrange(request):
    customer_data = Customer.objects.get(username=request.user.username)
    bannerr = Banner.objects.all()
    global km_range
    km_range = 5
    allcategories = AllCategories.objects.all()
    print("AllCategories", allcategories)
    if request.method == "POST":
        km_range = request.POST.get('km_range')
        allAddress = CustAddress.objects.filter(customer=customer_data)
        print(allAddress)
        ref_location = allAddress[0].location
        NearBySellers = Seller.objects.filter(location__dwithin=(ref_location, D(km=km_range)))
        print('NearBySellers', NearBySellers)
        return render(request, 'customer/dashboard.html',
                      {'customer_data': customer_data, 'near_by_sellers': NearBySellers,
                       'allcategories': allcategories, })


@login_required(login_url='custLogin')
def custDashboard(request):
    customer_data = Customer.objects.get(username=request.user.username)
    bannerr = Banner.objects.all()
    global km_range
    km_range = 1000000
    allcategories = AllCategories.objects.all()
    if request.method == "POST":
        km_range = request.POST.get('km_range')
    allAddress = CustAddress.objects.filter(customer=customer_data)
    if len(allAddress) == 0:
        ref_location = None
        cus_add = None
        NearBySellers = None
        nn=None
    else:
        ref_location = allAddress[0].location
        cus_add = allAddress[0]
        NearBySellers = Seller.objects.filter(location__dwithin=(ref_location, D(km=km_range)))
        # NearBySellers = list(Seller.objects.filter(location__dwithin=(ref_location, D(km=km_range))))
        nn = list(NearBySellers.values("shopname", "location", 'shop_image', 'username','avarage_review'))

        for i in range(len(NearBySellers)):
            origin = (ref_location[0], ref_location[1])
            dist = (NearBySellers[i].location[0], NearBySellers[i].location[1])
            dist1 = geodesic(origin, dist).kilometers.__round__(2)
            nn[i]['dis'] = dist1

    if nn is None:
        sorted_nn=None
    else:
        sorted_nn = sorted(nn, key=lambda d: d['dis'])

    return render(request, 'customer/dashboard.html',
                  {'customer_data': customer_data, 'near_by_sellers': sorted_nn, 'customer_add': ref_location,
                   'cus_add': cus_add,
                   'allcategories': allcategories, 'bannerr': bannerr})


@login_required(login_url='custLogin')
def searchProductNearBY(request):
    cus_add = base(request)
    customer_data = Customer.objects.get(username=request.user.username)
    global km_range
    allcategories = AllCategories.objects.all()

    try:
        allAddress = CustAddress.objects.filter(customer=customer_data)
        ref_location = allAddress[0].location

        if request.method == "POST":

            category_name = request.POST.get('category_name')
            product_name = request.POST.get('product_name')

            print(km_range, "--", category_name, "--", product_name)

            if km_range is None or km_range == '':
                km_range = 5

            if category_name is not None:
                NearBySellers = Seller.objects.filter(location__dwithin=(ref_location, D(km=km_range)),
                                                      categories_list__icontains=category_name)
            if product_name is not None:
                NearByProducts = Product.objects.filter(
                    location__dwithin=(ref_location, D(km=km_range)),
                    product_name__icontains=product_name)

                list_seller_cr = []
                for product in NearByProducts:
                    if product.seller_cr not in list_seller_cr:
                        list_seller_cr.append(product.seller_cr)

                NearBySellers = []

                for seller_cr in list_seller_cr:
                    NearBySellers.append(Seller.objects.get(credentials_id=seller_cr))

            print('NearBySellers', NearBySellers)
            return render(request, 'customer/searchresult.html',
                          {'customer_data': customer_data, 'near_by_sellers': NearBySellers,
                           'allcategories': allcategories, 'cus_add': cus_add})

        NearBySellers = Seller.objects.filter(location__dwithin=(ref_location, D(km=km_range)))
        print('NearBySellers', NearBySellers)

        return render(request, 'customer/searchresult.html',
                      {'customer_data': customer_data, 'near_by_sellers': NearBySellers,
                       'allcategories': allcategories})
    except:
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


import ast


def sellerlandingpage(request):
    if request.method == "GET":
        allow_user_to_give_review = False

        seller_detail = Seller.objects.get(username=request.GET["seller_name"])
        seller_cat = seller_detail.categories_list
        seller_cat = ast.literal_eval(seller_cat)

        loc = seller_detail.location
        seller_id = seller_detail.credentials_id

        try:
            product_category = request.GET["category"]
            seller_products = Product.objects.filter(seller_cr=seller_id, is_featured=True,
                                                     product_category=product_category)
        except MultiValueDictKeyError:
            seller_products = Product.objects.filter(seller_cr=seller_id, is_featured=True)

        customer = Customer.objects.get(username=request.user.username)

        access_review_to_seller_string_list = customer.access_review_to_seller_list
        access_review_to_seller_list = ast.literal_eval(access_review_to_seller_string_list)

        print('access_review_to_seller_list', access_review_to_seller_list)

        if seller_id in access_review_to_seller_list:
            allow_user_to_give_review = True

        cus_add = base(request)
        # print(seller_detail.location[0],seller_detail.location[1])
        # print(cus_add.location[0],cus_add.location[1])

        origin = (seller_detail.location[0], seller_detail.location[1])  # (latitude, longitude) don't confuse
        dist = (cus_add.location[0], cus_add.location[1])
        distance = geodesic(origin, dist).kilometers.__round__(2)
        print(distance)

        data = {
            'products': seller_products,
            'customer': customer,
            'seller_cat': seller_cat,
            'seller_id': seller_id,
            'seller_detail': seller_detail,
            'loc': loc,
            'cus_add': cus_add,
            'distance': distance,
            'allow_user_to_give_review': allow_user_to_give_review
        }

        print("sellerlandingpage-Data", data)

    elif request.method == "POST":
        rating = int(request.POST['rating'])

        seller_detail = Seller.objects.get(credentials_id=request.POST["seller_id"])
        total_stars = seller_detail.total_stars + rating
        total_reviews = seller_detail.total_reviews + 1
        avarage_review = round(total_stars/total_reviews, 1)

        seller_detail.total_stars = total_stars
        seller_detail.total_reviews = total_reviews
        seller_detail. avarage_review = avarage_review
        seller_detail.save()

        allow_user_to_give_review = False
        seller_cat = seller_detail.categories_list
        seller_cat = ast.literal_eval(seller_cat)

        loc = seller_detail.location
        seller_id = seller_detail.credentials_id

        try:
            product_category = request.GET["category"]
            seller_products = Product.objects.filter(seller_cr=seller_id, is_featured=True,
                                                     product_category=product_category)
        except MultiValueDictKeyError:
            seller_products = Product.objects.filter(seller_cr=seller_id, is_featured=True)

        customer = Customer.objects.get(username=request.user.username)

        access_review_to_seller_string_list = customer.access_review_to_seller_list
        access_review_to_seller_list = ast.literal_eval(access_review_to_seller_string_list)

        print('access_review_to_seller_list', access_review_to_seller_list)

        if seller_id in access_review_to_seller_list:
            access_review_to_seller_list.remove(seller_id)

        customer.access_review_to_seller_list = str(access_review_to_seller_list)
        customer.save()

        cus_add = base(request)
        # print(seller_detail.location[0],seller_detail.location[1])
        # print(cus_add.location[0],cus_add.location[1])

        origin = (seller_detail.location[0], seller_detail.location[1])  # (latitude, longitude) don't confuse
        dist = (cus_add.location[0], cus_add.location[1])
        distance = geodesic(origin, dist).kilometers.__round__(2)
        print(distance)

        data = {
            'products': seller_products,
            'customer': customer,
            'seller_cat': seller_cat,
            'seller_id': seller_id,
            'seller_detail': seller_detail,
            'loc': loc,
            'cus_add': cus_add,
            'distance': distance,
            'allow_user_to_give_review': allow_user_to_give_review
        }

        print("sellerlandingpage-review-Data", data)

    return render(request, 'customer/sellerlandingpage.html', data)


def base(request):
    customer_data = Customer.objects.get(username=request.user.username)
    global km_range
    if request.method == "POST":
        km_range = request.POST.get('km_range')
    allAddress = CustAddress.objects.filter(customer=customer_data)
    if len(allAddress) == 0:
        cus_add = None
    else:
        cus_add = allAddress[0]
    return cus_add


def cart(request):
    cus_add = base(request)
    return render(request, 'customer/cart.html', {'cus_add': cus_add})


def confirm(request):
    if request.method == "POST":
        name = request.POST.get('name')
        list_of_orders = request.POST.get('product_list')
        order_type = request.POST.get('order_type')
        pick_up_time = request.POST.get('pick_up_time')
        total = request.POST.get('total')
        amount = int(total)
        print(amount)
        return render(request, 'customer/checkout.html',
                      {'list_of_orders': list_of_orders, 'name': name, 'total': int(total), 'amount': int(amount) * 100,
                       'order_type': order_type, 'pick_up_time': pick_up_time})
    else:
        return render(request, 'customer/cart.html')


def checkout(request):
    if request.method == "POST":
        order_type = request.POST.get('order_type')
        pick_up_date = request.POST.get('pick_up_date')

        if pick_up_date == '':
            pick_up_date = None

        amount = int(request.POST.get('total').replace('/', '')) / 100
        list_of_orders = request.POST.get('list_of_orders').replace('/', '')

        client = razorpay.Client(auth=("rzp_test_bSTKVqtv6GwTso", "YEAj0ll32SLlXhunbTJSJqVH"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        customer_data = Customer.objects.get(username=request.user.username)

        access_review_to_seller_string_list = customer_data.access_review_to_seller_list
        access_review_to_seller_list = ast.literal_eval(access_review_to_seller_string_list)

        seller_id = Product.objects.get(pk=json.loads(list_of_orders)[0]['proid']).seller_cr

        if seller_id not in access_review_to_seller_list:
            access_review_to_seller_list.append(seller_id)

        customer_data.access_review_to_seller_list = str(access_review_to_seller_list)
        customer_data.save()

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
    return redirect('custDashboard', data)


def orders(request):
    cus_add = base(request)
    order_data = AllOrders.objects.all().filter(customer_id=request.user.id)
    data = {
        'order_data': order_data,
        'cus_add': cus_add,
    }

    return render(request, "customer/myorderview.html", data)


@login_required(login_url='cusLogin')
def profile(request):
    cus_add = base(request)
    if request.method == 'GET':
        customer_data = Customer.objects.get(credentials_id=request.user.id)
        profile_to_be_edit = Customer.objects.get(credentials_id=request.user.id)
        return render(request, 'customer/profileview.html',
                      {'profile_to_be_edit': profile_to_be_edit, 'customer_data': customer_data, 'cus_add': cus_add})

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
