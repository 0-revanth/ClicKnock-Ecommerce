from django.db import models
import os

class users(models.Model):
    FirstName = models.CharField(max_length=120, null=True, blank=True)
    LastName = models.CharField(max_length=120, null=True, blank=True)
    Email = models.EmailField(max_length=120, unique=True)
    PhoneNumber = models.CharField(max_length=10, unique=True, null=True, blank=True)
    Gender = models.CharField(max_length=120, blank=True, null=False)
    Password = models.CharField(max_length=200, null=True, blank=True)
    UserType = models.CharField(default='C', max_length=1)
    profile_picture = models.ImageField(upload_to='images/profile_pics/', blank=True, null=True)
    

    def delete(self, *args, **kwargs):
        if self.profile_picture and os.path.isfile(self.profile_picture.path):
            os.remove(self.profile_picture.path)
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.Email  # ✅ New

class seller(models.Model):
    FirstName = models.CharField(max_length=120, null=True, blank=True)
    LastName = models.CharField(max_length=120, null=True, blank=True)
    Email = models.EmailField(max_length=120, unique=True)
    PhoneNumber = models.CharField(max_length=10, unique=True, null=True, blank=True)
    Gender = models.CharField(max_length=120, blank=True, null=False)
    Password = models.CharField(max_length=200, null=True, blank=True)
    UserType = models.CharField(default='S', max_length=1)
    SellerID = models.CharField(max_length=50, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="images/profile_pics/", null=True, blank=True)


    def delete(self, *args, **kwargs):
        if self.profile_picture and os.path.isfile(self.profile_picture.path):
            os.remove(self.profile_picture.path)
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.Email 