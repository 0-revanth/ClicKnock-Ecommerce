from django.db import models

class users(models.Model):
    FirstName = models.CharField(max_length=120,null=True,blank=True)
    LastName = models.CharField(max_length=120,null=True,blank=True)
    Email = models.EmailField(max_length=120 ,blank=False,null=False,unique=True)
    PhoneNumber = models.CharField(max_length=10,null=True,blank=True,unique=True)
    Gender = models.CharField(max_length=120 ,blank=True,null=False)
    Password = models.CharField(max_length=200,null=True,blank=True)
    UserType=models.CharField(default='C',max_length=1)

    def __str__(self):
        return self.Email
    
class seller(models.Model):
    FirstName = models.CharField(max_length=120,null=True,blank=True)
    LastName = models.CharField(max_length=120,null=True,blank=True)
    Email = models.EmailField(max_length=120 ,blank=False,null=False,unique=True)
    PhoneNumber = models.CharField(max_length=10,null=True,blank=True,unique=True)
    Gender = models.CharField(max_length=120 ,blank=True,null=False)
    Password = models.CharField(max_length=200,null=True,blank=True)
    UserType=models.CharField(default='S',max_length=1)

    def __str__(self):
        return self.Email