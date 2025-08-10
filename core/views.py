from django.http import HttpRequest
from .models import *
from loginreg.models import *
from django.contrib import messages
from django.http import JsonResponse
import json
from django.contrib.auth import logout as auth_logout
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import os




# Create your views here.
from django.shortcuts import render
from .models import Product # Assuming your Product model is in models.py

def Home(request, *args, **kwargs):
    # Fetch all products (you might want to order them if the "first 5" matters)
    all_products = Product.objects.all().order_by('id') # Example: order by ID

    # Initialize lists for each category's top 5 products
    Electronics = []
    Fashion = []
    Home = []
    Beauty= []
    Sports = []
    Books = []

    # Populate the lists, ensuring each gets no more than 5 products
    for product in all_products:
        category_code = product.Category # Assuming 'Category' stores the single letter code (E, F, HK, etc.)

        if category_code == 'E' and len(Electronics) < 5:
            Electronics.append(product)
        elif category_code == 'F' and len(Fashion) < 5:
            Fashion.append(product)
        elif category_code == 'HK' and len(Home) < 5:
            Home.append(product)
        elif category_code == 'BT' and len(Beauty) < 5:
            Beauty.append(product)
        elif category_code == 'S' and len(Sports) < 5:
            Sports.append(product)
        elif category_code == 'BK' and len(Books) < 5:
            Books.append(product)

    # Prepare the context dictionary with your new variables
    Context = {
    'Electronics': Electronics,
    'Fashion': Fashion,
    'Home': Home,
    'Beauty': Beauty,
    'Sports': Sports,
    'Books': Books,
    'user_type': request.session.get('user_type', ''),
    'user_id': request.session.get('user_id', '')
}

    return render(request, 'home.html', Context)

def Cart(request, *args, **kwargs):
    if 'user_id' in request.session:
        try:
            customer = users.objects.get(id=request.session['user_id'])
            order, created = Order.objects.get_or_create(users=customer, Complete=False)
            items = order.orderitem_set.all()

            # Calculate total amount
            total = sum(item.Product.DiscountPrice * item.Quantity for item in items)

        except users.DoesNotExist:
            items = []
            order = None
            total = 0
    else:
        items = []
        order = None
        total = 0

    context = {
        'items': items,
        'order': order,
        'total': total,
    }
    return render(request, 'cart.html', context)


def Addproduct(request,*args,**kwargs):
    if request.method=='POST':
        product_name = request.POST.get('name')
        sid= request.POST.get('sid')
        price = request.POST.get('price')
        category = request.POST.get('category')
        specs = request.POST.get('specs')
        discountprice = request.POST.get('discount')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')  

        
        if Product.objects.filter(Name=product_name).exists():
            messages.error(request, "Name already exists")


        try:
            
            product= Product.objects.create(
                Name=product_name,
                SellerID=sid,
                Price=price,
                Category=category,
                Specs=specs,
                DiscountPrice=discountprice,
                Rating=rating,
                Image=image
            )
            product.save()
            messages.success(request,"Successfully uploaded")
            
        except:
            messages.error(request,"Error Occured,Try again")
    return render(request,'addproduct.html',{})





def UserProfile(request, *args, **kwargs):
    if request.session.get('user_type') != 'customer' or 'user_id' not in request.session:
        return redirect('login')  # Redirect if not a logged-in customer

    try:
        customer = users.objects.get(id=request.session['user_id'])

        # Recent orders for this user
        orders = Order.objects.filter(users=customer).order_by('-DateOrderd')[:5]

        # Latest address (if available)
        address = ShippingAddress.objects.filter(users=customer).last()

        context = {
            'user': customer,
            'orders': orders,
            'address': address
        }
        return render(request, 'uprofile.html', context)

    except users.DoesNotExist:
        return redirect('login')



def List(request, *args, **kwargs):
    category_code = request.GET.get('category')  # Example: 'E', 'F', 'HK', etc.
    
    if category_code:
        products = Product.objects.filter(Category=category_code)
        category_name = dict(CATEGORY_CHOICES).get(category_code, "All Products")
    else:
        products = Product.objects.all()
        category_name = "All Products"

    context = {
        'products': products,
        'category_name': category_name
    }
    return render(request, 'list.html', context)





def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Product ID:', productId)
    print('Action:', action)

    try:
        customer = users.objects.get(id=request.session['user_id'])
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(users=customer, Complete=False)

        orderItem, created = OrderItem.objects.get_or_create(Order=order, Product=product)

        if action == 'add':
            orderItem.Quantity = (orderItem.Quantity + 1)
        elif action == 'remove':
            orderItem.Quantity = (orderItem.Quantity - 1)

        orderItem.save()

        if orderItem.Quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was updated', safe=False)

    except Exception as e:
        print("Error:", e)
        return JsonResponse({'error': str(e)}, status=400)


def CheckOut(request,*args,**kwargs):
    return render(request,'checkout.html',{})




def ProductDetail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        related_products = Product.objects.filter(
            Category=product.Category
        ).exclude(id=product.id)[:6]

        category_name = dict(CATEGORY_CHOICES).get(product.Category, "Products")

        context = {
            'product': product,
            'related_products': related_products,
            'category_name': category_name
        }
        return render(request, 'product.html', context)
    except Product.DoesNotExist:
        return redirect('Home')



def SellerProfile(request, *args, **kwargs):
    if request.session.get('user_type') != 'seller' or 'seller_id' not in request.session:
        return redirect('login')  # Redirect if not logged in as seller

    try:
        # Get seller object
        seller_user = seller.objects.get(id=request.session['seller_id'])

        # Get seller's store address
        try:
            store_address = StoreAddress.objects.get(seller=seller_user)
        except StoreAddress.DoesNotExist:
            store_address = None  # Handle gracefully if not set

        # Get active listings
        active_listings = Product.objects.filter(SellerID=seller_user.SellerID)
        active_listings_count = active_listings.count()

        # Get related orders for seller's products
        orders = Order.objects.filter(orderitem__Product__SellerID=seller_user.SellerID).distinct()

        # Calculate total sales: sum of (DiscountPrice * Quantity) for all seller's order items
        order_items = OrderItem.objects.filter(Product__SellerID=seller_user.SellerID)
        total_sales = order_items.aggregate(total=Sum(F('Quantity') * F('Product__DiscountPrice')))['total'] or 0

        # Pending orders
        pending_orders_count = orders.filter(Complete=False).count()

        context = {
            'user': seller_user,
            'store_address': store_address,
            'total_sales': round(total_sales, 2),
            'active_listings': active_listings_count,
            'pending_orders': pending_orders_count,
        }

        return render(request, 'sprofile.html', context)

    except seller.DoesNotExist:
        return redirect('login')
    





def edit_user_profile(request):
    if request.session.get('user_type') != 'customer' or 'user_id' not in request.session:
        return redirect('login')

    user_obj = get_object_or_404(users, id=request.session['user_id'])

    if request.method == "POST":
        user_obj.FirstName = request.POST.get('FirstName', user_obj.FirstName)
        user_obj.LastName = request.POST.get('LastName', user_obj.LastName)
        user_obj.Gender = request.POST.get('Gender', user_obj.Gender)
        if 'profile_picture' in request.FILES:
    # delete old file if exists
            if user_obj.profile_picture and os.path.isfile(user_obj.profile_picture.path):
                os.remove(user_obj.profile_picture.path)
                user_obj.profile_picture = request.FILES['profile_picture']

        # Email & PhoneNumber remain read-only
        user_obj.save()

        return render(request, 'editprofile.html', {
        'customer': user_obj,
        'success': True
        })


    return render(request, 'editprofile.html', {'customer': user_obj})


def edit_seller_profile(request):
    if request.session.get('user_type') != 'seller' or 'seller_id' not in request.session:
        return redirect('login')

    seller_obj = get_object_or_404(seller, id=request.session['seller_id'])

    if request.method == "POST":
        seller_obj.FirstName = request.POST.get('FirstName', seller_obj.FirstName)
        seller_obj.LastName = request.POST.get('LastName', seller_obj.LastName)
        seller_obj.Gender = request.POST.get('Gender', seller_obj.Gender)
        if 'profile_picture' in request.FILES:
    # delete old file if exists
            if seller_obj.profile_picture and os.path.isfile(seller_obj.profile_picture.path):
                os.remove(seller_obj.profile_picture.path)
                seller_obj.profile_picture = request.FILES['profile_picture']

        # Email & PhoneNumber remain read-only
        seller_obj.save()

        return render(request, 'editprofile.html', {
        'customer': seller_obj,
        'success': True
        })

    return render(request, 'editprofile.html', {'customer': seller_obj})




def logout_view(request):
    auth_logout(request)  # Clears Django's session auth
    request.session.flush()  # Clears all session data
    return redirect('Home')  # Replace 'login' with your actual login page name
