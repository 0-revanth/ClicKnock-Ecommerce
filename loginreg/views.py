from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import *

def login(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to log in a customer
        user = users.objects.filter(
            models.Q(Email=username) | models.Q(PhoneNumber=username),
            Password=password
        ).first()

        if user:
            request.session['user_id'] = user.id
            request.session['user_type'] = 'customer'
            messages.success(request, "Login successful!")
            return redirect('Home')

        # Try to log in a seller
        seller_user = seller.objects.filter(
            models.Q(Email=username) | models.Q(PhoneNumber=username),
            Password=password
        ).first()

        if seller_user:
            request.session['seller_id'] = seller_user.id
            request.session['user_type'] = 'seller'
            messages.success(request, "Login successful!")
            return redirect('Home')

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {})



def register(request,*args,**kwargs):

    if request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender=request.POST.get('gender')
        password=request.POST.get('password')
        
        if users.objects.filter(Email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register') 

        
        if users.objects.filter(PhoneNumber=phone).exists():  
            messages.error(request, "Phone number already exists")
            return redirect('register')

        try:
            
            user= users.objects.create(
                FirstName=first_name,
                LastName=last_name,
                Email=email,
                PhoneNumber=phone,
                Gender=gender,
                Password=password
            )
            user.save()
            messages.success(request,"Successfully Registered")
            return redirect('login')
            
        except:
            messages.error(request,"Error Occured,Try again")
    

    return render(request,"register.html",{})



def seller_register(request,*args,**kwargs):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        
        if seller.objects.filter(Email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register') 

        if seller.objects.filter(PhoneNumber=phone).exists():  
            messages.error(request, "Phone number already exists")
            return redirect('register')

        try:
            seller_id_value = phone + "@ck"

            Seller = seller.objects.create(
                FirstName=first_name,
                LastName=last_name,
                Email=email,
                PhoneNumber=phone,
                Gender=gender,
                Password=password,
                SellerID=seller_id_value  # ✅ assigned here
            )
            Seller.save()
            messages.success(request, "Successfully Registered")
            return redirect('login')
            
        except:
            messages.error(request, "Error Occurred, Try again")
    
    return render(request, "sellerreg.html", {})



# Create your views here.
