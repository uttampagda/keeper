from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Customer
from django.contrib import messages, auth

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

def custDashboard(request):
    if request.user.is_authenticated:
        customer_data = Customer.objects.get(username=request.user.username)
        return render(request, 'customer/dashboard.html', {'customer_data':customer_data})
    else:
        redirect('custLogin')

def custLogout(request):
    logout(request)
    return redirect('custhome')

def custhome(request):
    return render(request,'customer/home.html')