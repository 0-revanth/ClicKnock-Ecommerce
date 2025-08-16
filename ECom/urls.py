"""
URL configuration for ECom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from loginreg.views import login,register,seller_register
from core.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name='Home'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('seller_register/',seller_register,name='seller_register'),
    path('home/',Home,name='Home'),
    path('cart/',Cart,name='Cart'),
    path('addproduct/',Addproduct,name='Addproduct'),
    path('uprofile/',UserProfile,name='uprofile'),
    path('sprofile/',SellerProfile,name='sprofile'),
    path('edit-user-profile/',edit_user_profile, name='edit_user_profile'),
    path('edit-seller-profile/',edit_seller_profile, name='edit_seller_profile'),
    path('change-user-address/', change_user_address, name='change_user_address'),
    path('change-store-address/', change_store_address, name='change_store_address'),
    path('list/',List,name='List'),
    path('update_item/',updateItem,name='update_item'),
    path('checkout/',CheckOut,name='checkout'),
    path('product/<int:product_id>/', ProductDetail, name='product_detail'),
    path('logout/',logout_view, name='logout'),

    



]


urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


