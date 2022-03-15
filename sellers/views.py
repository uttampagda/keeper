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
import ast
from django.utils.datastructures import MultiValueDictKeyError


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
                return redirect('sellerDashboard')
            else:
                messages.warning(request, 'You are not seller')
                return redirect('sellerLogin')
        else:
            messages.warning(request, 'Please enter valid details!')
            return redirect('sellerLogin')

    return render(request, 'seller/login.html')


@login_required(login_url='sellerLogin')
def sellerDashboard(request):
    print(request.user.id)
    if request.user.is_authenticated:
        seller_data = Seller.objects.get(credentials_id=request.user.id)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=24)

        order_status_dic = {
            "PENDING": 0,
            "ACCEPTED": 0,
            "REJECTED": 0,
            "COMPLETE": 0
        }
        for order_status in order_status_dic.keys():
            order_status_dic[order_status] = AllOrders.objects.filter(seller_id=request.user.id,
                                                                      created_date__year=now.year,
                                                                      created_date__month=now.month,
                                                                      created_date__day=now.day,
                                                                      order_status=order_status).count()
        #for Chart part
        total_orders_30 = []
        chartdate = []
        for day in range(0, 29):
            earlier = now - datetime.timedelta(days=day)
            total_orders_30.append(
                AllOrders.objects.filter(seller_id=request.user.id, created_date__year=earlier.year,
                                         created_date__month=earlier.month, created_date__day=earlier.day).count())
            date = str(earlier.day) + ' ' + str(earlier.strftime('%B'))+ ' ' + str(earlier.year)
            chartdate.append(date)

        if total_orders_30[0]==total_orders_30[1]:
            today_orderper = 0
        elif total_orders_30[1]==0:
            today_orderper = 0
        elif total_orders_30[0]>total_orders_30[1]:
            today_orderper = (total_orders_30[0]//total_orders_30[1]) * 50
        else:
            today_orderper = '-0'

        new_orders = AllOrders.objects.filter(seller_id=request.user.id, created_date__range=(earlier, now),
                                              is_rejected=False).exclude(is_accepted=True)
        accepted_orders = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=True, is_rejected=False)
        rejected_order = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=False, is_rejected=True)

        data = {
            'seller_data': seller_data,
            'new_orders': new_orders,
            'accepted_orders': accepted_orders,
            'rejected_order': rejected_order,
            'order_status_dic': order_status_dic,
            'total_orders_30': total_orders_30,
            'chartdate': chartdate,
            'today_orderper': today_orderper
        }
        return render(request, 'seller/seller.html', data)
    else:
        redirect('sellerLogin')


def sellerLogout(request):
    logout(request)
    return redirect('sellerLogin')


@login_required(login_url='sellerLogin')
def sellerhome(request):
    return redirect('sellerDashboard')


@login_required(login_url='sellerLogin')
def addproduct(request):
    seller_data = Seller.objects.get(credentials_id=request.user.id)

    if request.method == 'POST':
        seller_data = Seller.objects.get(credentials_id=request.user.id)
        product_name = request.POST['product_name']
        price = request.POST['price']
        category = request.POST['category']
        product_disc = request.POST['product_disc']
        seller_cr = request.user.id
        product_image = request.FILES['productImage']

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

        categories_list = ast.literal_eval(seller_data.categories_list)
        if category not in categories_list:
            categories_list.append(category)

        seller_data.categories_list = str(categories_list)
        seller_data.save()

        return redirect('products')

    allCategories = AllCategories.objects.all()

    data = {
        'allCategories': allCategories,
        'seller_data': seller_data,
    }
    return render(request, 'seller/addproductview.html', data)


@login_required(login_url='sellerLogin')
def acceptOrder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            order_id = request.POST['order_id']
            acceptOrd = AllOrders.objects.get(id=order_id)
            acceptOrd.is_accepted = True
            acceptOrd.order_status = "ACCEPTED"
            acceptOrd.is_rejected = False
            acceptOrd.save()

        order_status = 'ALL'
        if request.method == "GET" and len(request.GET) > 0:
            order_status = request.GET['order_status']

        seller_data = Seller.objects.get(credentials_id=request.user.id)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=6000)

        if order_status == "ALL":
            orders = AllOrders.objects.filter(seller_id=request.user.id)
        elif order_status == "PENDING":
            orders = AllOrders.objects.filter(seller_id=request.user.id, created_date__range=(earlier, now), is_rejected=False, order_status="PENDING")
        elif order_status == "ACCEPTED":
            orders = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=True, is_rejected=False, order_status="ACCEPTED")
        elif order_status == "REJECTED":
            orders = AllOrders.objects.filter(seller_id=request.user.id, order_status="REJECTED")
        elif order_status == "DELIVERED":
            orders = AllOrders.objects.filter(seller_id=request.user.id,  order_status=str("DELIVERED"))
        elif order_status == "SHIPPED":
            orders = AllOrders.objects.filter(seller_id=request.user.id, order_status=str('SHIPPED'))

        return render(request, 'seller/orderview.html', {'seller_data': seller_data, 'orders': orders})

    else:
        redirect('sellerLogin')


@login_required(login_url='sellerLogin')
def rejectOrder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            order_id = request.POST['order_id']
            rejectedOdr = AllOrders.objects.get(id=order_id)
            rejectedOdr.is_rejected = True
            rejectedOdr.order_status = "REJECTED"
            rejectedOdr.is_accepted = False
            rejectedOdr.save()

        seller_data = Seller.objects.get(credentials_id=request.user.id)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=5)
        new_orders = AllOrders.objects.filter(seller_id=request.user.id, created_date__range=(earlier, now),
                                              is_rejected=None).exclude(is_accepted=True)
        accepted_orders = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=True, is_rejected=False)
        rejected_order = AllOrders.objects.filter(seller_id=request.user.id, is_accepted=False, is_rejected=True)

        return render(request, 'seller/orderview.html',
                      {'seller_data': seller_data, 'new_orders': new_orders, 'accepted_orders': accepted_orders,
                       'rejected_order': rejected_order})
    else:
        redirect('sellerLogin')

@login_required(login_url='sellerLogin')
def editstatus(request):
    if request.method == 'POST':
        status_to_update = request.POST['status']
        or_id = request.POST['or_id']
        print("here",status_to_update,or_id)
        accepted_order = AllOrders.objects.get(seller_id=request.user.id, id=or_id)
        accepted_order.order_status=status_to_update
        accepted_order.save()
        print("order status is updated")
    return redirect('acceptOrder')

@login_required(login_url='sellerLogin')
def vieworderdetails(request):
    new_orders = AllOrders.objects.filter(seller_id=request.user.id,is_rejected=None).exclude(is_accepted=True)
    return render(request, 'seller/vieworderdeatils.html', new_orders)

@login_required(login_url='sellerLogin')
def products(request):
    if request.user.is_authenticated:
        seller_data = Seller.objects.get(credentials_id=request.user.id)
        products = Product.objects.filter(shopname=seller_data.shopname)

        allCategories = AllCategories.objects.all()

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

        seller_data = Seller.objects.get(credentials_id=request.user.id)
        product_to_be_edit = Product.objects.get(id=product_id)
        allCategories = AllCategories.objects.all()
        data = {
            'seller_data': seller_data,
            'product_to_be_edit': product_to_be_edit,
            'allCategories': allCategories
        }
        return render(request, 'seller/editProductview.html', data)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        delete_product = request.POST.get('delete_product')

        if delete_product == "True":
            Product.objects.get(id=product_id).delete()

            return redirect('products')

        product_to_be_edit = Product.objects.get(id=product_id)

        product_to_be_edit.product_name = request.POST.get('product_name')
        product_to_be_edit.price = request.POST.get('price')
        product_to_be_edit.product_category = request.POST.get('category')
        product_to_be_edit.product_disc = request.POST.get('product_disc')

        try:
            product_to_be_edit.product_image = request.FILES['productImage']
        except MultiValueDictKeyError:
            print("error")

        if request.POST.get('is_featured') == "on" and request.POST.get('not_featured') == None:
            is_featured = True
        elif request.POST.get('is_featured') == None and request.POST.get('not_featured') == "on":
            is_featured = False
        else:
            is_featured = True

        product_to_be_edit.is_featured = is_featured
        product_to_be_edit.save()

        return redirect('products')


@login_required(login_url='sellerLogin')
def editProfile(request):
    if request.method == 'GET':
        seller_data = Seller.objects.get(credentials_id=request.user.id)
        profile_to_be_edit = Seller.objects.get(credentials_id=request.user.id)
        return render(request, 'seller/Profileview.html',
                      {'profile_to_be_edit': profile_to_be_edit, 'seller_data': seller_data})

    if request.method == 'POST':
        profile_to_be_edit = Seller.objects.get(credentials_id=request.user.id)

        newpassword = request.POST.get('newpassword')
        newconfirmpassword = request.POST.get('newconfirmpassword')
        if newpassword != "" and newconfirmpassword != "" and newpassword == newconfirmpassword:
            u = User.objects.get(id=request.user.id)
            u.set_password(newpassword)
            u.save()
            print("password updated")

        profile_to_be_edit.shopname = request.POST.get('shopname')
        profile_to_be_edit.phone = request.POST.get('phone')
        profile_to_be_edit.shop_image = request.FILES.get('profileImage')

        profile_to_be_edit.save()
        return redirect('sellerDashboard')

@login_required(login_url='sellerLogin')
def orderdetails(request,id):
    if request.method == 'GET':
        seller_data = Seller.objects.get(credentials_id=request.user.id)
        allord=AllOrders.objects.get(id=id)
        detail=ast.literal_eval(allord.order_details)



        orderdetailsd = {
            'seller_data': seller_data,
            'detail':detail,
            'allord':allord
        }
        return render(request, 'seller/vieworderdeatils.html', orderdetailsd)

