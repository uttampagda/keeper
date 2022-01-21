import requests
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Seller, Product, AllCategories
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from customer.models import AllOrders
import datetime


# Create your views here.

def sellerRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        shopname = request.POST['shopname']
        email = request.POST['email']
        phone = request.POST['phone']
        latiLong = request.POST['latiLong'].split(',')
        print(request.POST['latiLong'])
        # TODO VALIDATION ON latLong check valid or not
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
                        password=password
                    )

                    user = Seller(
                        credentials=credentials,
                        shopname=shopname,
                        username=username,
                        email=email,
                        phone=phone,
                        location=Point(float(log), float(lat), srid=4326)
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
    print(request.user.id)
    if request.user.is_authenticated:
        seller_data = Seller.objects.get(credentials_id=request.user.id)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=5)
        new_orders = AllOrders.objects.filter(seller_id=request.user.id, created_date__range=(earlier, now),
                                              is_rejected=False).exclude(is_accepted=True)
        accepted_orders = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=True, is_rejected=False)
        rejected_order = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=False, is_rejected=True)
        print(new_orders, accepted_orders, rejected_order)

        data = {
            'seller_data': seller_data,
            'new_orders': new_orders,
            'accepted_orders': accepted_orders,
            'rejected_order': rejected_order
        }
        return render(request, 'seller/seller.html', data)
    else:
        redirect('sellerLogin')


def sellerLogout(request):
    logout(request)
    return redirect('sellerLogin')

@login_required(login_url='sellerLogin')
def sellerhome(request):
    return render(request, 'seller/seller.html')


@login_required(login_url='sellerLogin')
def addproduct(request):
    print(request.user.id)

    if request.method == 'POST':
        seller_data = Seller.objects.get(credentials_id=request.user.id)
        product_name = request.POST['product_name']
        price = request.POST['price']
        category = request.POST['category']
        product_image = request.FILES['productImage']
        product_disc = request.POST['product_disc']
        seller_cr = request.user.id
        addproduct = Product(
            seller_cr=seller_cr,
            product_name=product_name,
            price=price,
            location=seller_data.location,
            shopname=seller_data.shopname,
            product_image=product_image,
            product_category=category,
            product_disc=product_disc,
        )

        addproduct.save()
        print('saved')
        return redirect('products')

    allCategories = AllCategories.objects.all()

    data = {
        'allCategories': allCategories
    }
    return render(request, 'seller/addproductview.html', data)

@login_required(login_url='sellerLogin')
def acceptOrder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            order_id = request.POST['order_id']
            acceptOrd = AllOrders.objects.get(id=order_id)
            acceptOrd.is_accepted = True
            acceptOrd.is_rejected = False
            acceptOrd.save()

        seller_data = Seller.objects.get(credentials_id=request.user.id)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=5)
        new_orders = AllOrders.objects.filter(seller_id=request.user.id, created_date__range=(earlier, now),
                                              is_rejected=None).exclude(is_accepted=True)
        accepted_orders = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=True, is_rejected=False)
        rejected_order = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=False, is_rejected=True)
        print(new_orders, accepted_orders, rejected_order)
        return render(request, 'seller/orderview.html',
                      {'seller_data': seller_data, 'new_orders': new_orders, 'accepted_orders': accepted_orders,
                       'rejected_order': rejected_order})
    else:
        redirect('sellerLogin')


@login_required(login_url='sellerLogin')
def rejectOrder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            order_id = request.POST['order_id']
            rejectedOdr = AllOrders.objects.get(id=order_id)
            rejectedOdr.is_rejected = True
            rejectedOdr.is_accepted = False
            rejectedOdr.save()

        seller_data = Seller.objects.get(credentials_id=request.user.id)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=5)
        new_orders = AllOrders.objects.filter(seller_id=request.user.id, created_date__range=(earlier, now),
                                              is_rejected=None).exclude(is_accepted=True)
        accepted_orders = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=True, is_rejected=False)
        rejected_order = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=False, is_rejected=True)
        print(new_orders, accepted_orders, rejected_order)
        return render(request, 'seller/orderview.html',
                      {'seller_data': seller_data, 'new_orders': new_orders, 'accepted_orders': accepted_orders,
                       'rejected_order': rejected_order})
    else:
        redirect('sellerLogin')


@login_required(login_url='sellerLogin')
def products(request):
    if request.user.is_authenticated:
        seller_data = Seller.objects.get(credentials_id=request.user.id)
        products = Product.objects.filter(shopname=seller_data.shopname)

        allCategories = AllCategories.objects.all()
        print(allCategories)

        data = {
            'seller_data': seller_data,
            'products': products,
            'allCategories': allCategories
        }
        return render(request, 'seller/productview.html', data)
    else:
        redirect('sellerLogin')


@login_required(login_url='sellerLogin')
def editProducts(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')

        if product_id is None:
            seller_data = Seller.objects.get(credentials_id=request.user.id)
            products = Product.objects.filter(shopname=seller_data.shopname)

            data = {
                'products': products
            }
            return render(request, 'seller/productview.html', data)

        product_to_be_edit = Product.objects.get(id=product_id)
        allCategories = AllCategories.objects.all()
        return render(request, 'seller/editProductview.html', {'product_to_be_edit': product_to_be_edit, 'allCategories': allCategories})

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_to_be_edit = Product.objects.get(id=product_id)

        product_to_be_edit.product_name = request.POST.get('product_name')
        product_to_be_edit.price = request.POST.get('price')
        product_to_be_edit.product_category = request.POST.get('category')
        product_to_be_edit.product_disc = request.POST.get('product_disc')
        product_to_be_edit.save()

        seller_data = Seller.objects.get(credentials_id=request.user.id)
        products = Product.objects.filter(shopname=seller_data.shopname)
        return render(request, 'seller/productview.html', {'products': products})


@login_required(login_url='sellerLogin')
def editProfile(request):
    if request.method == 'GET':
        profile_to_be_edit = Seller.objects.get(credentials_id=request.user.id)
        return render(request, 'seller/Profileview.html', {'profile_to_be_edit': profile_to_be_edit})

    if request.method == 'POST':
        profile_to_be_edit = Seller.objects.get(credentials_id=request.user.id)

        profile_to_be_edit.shopname = request.POST.get('shopname')
        profile_to_be_edit.phone = request.POST.get('phone')
        profile_to_be_edit.email = request.POST.get('email')


        profile_to_be_edit.save()
        return render(request, 'seller/seller.html')