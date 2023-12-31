from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    braintree_id=models.CharField(max_length=255,blank=True,null=True)
    username=None
    is_active = models.BooleanField(default=True)
    is_staff=None
    last_login=None
    profile_pic=models.CharField(max_length=255,blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [first_name,last_name]