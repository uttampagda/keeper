from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Seller
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


# Create your views here.

def sellerRegister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        shopname = request.POST['shopname']
        email = request.POST['email']
        phone = request.POST['phone']
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
        seller_data = Seller.objects.get(username=request.user.username)
        return render(request, 'seller/dashboard.html', {'seller_data':seller_data})
    else:
        redirect('sellerLogin')

def sellerLogout(request):
    logout(request)
    return redirect('sellerhome')

def sellerhome(request):
    return render(request,'seller/home.html')
