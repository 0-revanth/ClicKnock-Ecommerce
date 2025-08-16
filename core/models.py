from django.db import models
from django.contrib.auth.models import User
from loginreg.models import *


CATEGORY_CHOICES = (
    ('E', 'Electronics'),
    ('F', 'Fashion'),
    ('HK', 'Home&Kitchen'),
    ('BT', 'Beauty'),
    ('S', 'Sports'),
    ('BK', 'Books')
)

# Create your models here.

class Product(models.Model):
    Name = models.CharField(max_length=200,null=True)
    SellerID = models.CharField(max_length=200,null=True)
    Price = models.FloatField()
    Category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    Specs = models.TextField(null=True,blank=True)
    DiscountPrice = models.FloatField()
    Rating = models.IntegerField(default=0,null=True,blank=True)
    Image = models.ImageField(blank=True,null=True,upload_to="images/product_images/")

    def __str__(self):
        return self.Name
    
    @property
    def ImageURL(self):
        try:
            url=self.Image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    users = models.ForeignKey(users, on_delete=models.SET_NULL,blank=True,null=True)
    DateOrderd = models.DateTimeField(auto_now_add=True)
    Complete = models.BooleanField(default=False,null=True,blank=False)
    TransactionId = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    Order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    Quantity = models.IntegerField(default=0,null=True,blank=True)
    DateAdded = models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    users = models.ForeignKey(users, on_delete=models.SET_NULL,blank=True,null=True)
    Order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    Address = models.CharField(max_length=200,null=True)
    City = models.CharField(max_length=200,null=True)
    State = models.CharField(max_length=200,null=True)
    Zip = models.CharField(max_length=200,null=True)
    DateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Address
    
class StoreAddress(models.Model):
    seller = models.OneToOneField(seller, on_delete=models.CASCADE)
    StoreName = models.CharField(max_length=200, null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    City = models.CharField(max_length=100, null=True, blank=True)
    State = models.CharField(max_length=100, null=True, blank=True)
    ZipCode = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.StoreName} - {self.City}, {self.State}"
