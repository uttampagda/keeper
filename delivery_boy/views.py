from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import DeliveryBoy
from django.contrib import messages, auth

# Create your views here.

def deliboyRegister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if DeliveryBoy.objects.filter(username=username).exists():
                messages.warning(request, 'Username exists')
                return redirect('deliboyRegister')
            else:
                if DeliveryBoy.objects.filter(email=email).exists():
                    messages.warning(request, 'email already exists')
                    return redirect('deliboyhome')
                else:
                    credentials = User.objects.create_user(
                        username=username,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )

                    user = DeliveryBoy(
                        credentials=credentials,
                        username=username,
                        email=email,
                        phone=phone,
                    )
                    user.save()
                    messages.success(request, 'Account created successfully')
                    return redirect('deliboyDashboard')
        else:
            messages.warning(request, 'Password do not match')
            return redirect('deliboyRegister')

    return render(request, 'deliveryBoy/register.html')

def deliboyLogin(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if DeliveryBoy.objects.filter(username=username).exists():
                    auth.login(request, user)
                    messages.warning(request, 'you are logged in')
                    return redirect('deliboyDashboard')
                else:
                    messages.warning(request, 'You are not delivery boy')
                    return redirect('deliboyLogin')
            else:
                messages.warning(request, 'invalid credentials')
                return redirect('deliboyLogin')
        return render(request, 'deliveryBoy/login.html')

def deliboyDashboard(request):
    if request.user.is_authenticated:
        deliveryBoy_data = DeliveryBoy.objects.get(username=request.user.username)
        return render(request, 'deliveryBoy/dashboard.html', {'deliveryBoy_data':deliveryBoy_data})
    else:
        redirect('deliboyLogin')

def deliboyLogout(request):
    logout(request)
    return redirect('deliboyhome')

def deliboyhome(request):
    return render(request,'deliveryBoy/home.html')
