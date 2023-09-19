from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.conf import settings

class Availability(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

class DatePricing(models.Model):
    date = models.DateField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Reservation(models.Model):
    user_id = models.PositiveIntegerField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    adult_numbers = models.PositiveIntegerField()
    children_numbers = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    is_family = models.BooleanField(default=False,blank=True,null=True)
    is_group = models.BooleanField(default=False,blank=True,null=True)
    is_couple = models.BooleanField(default=False,blank=True,null=True)
    guest_country = models.CharField(max_length=100,blank=True,null=True)
    guest_phone_number = models.CharField(max_length=100,blank=True,null=True)
    is_traveling_for_work = models.BooleanField(default=False,blank=True,null=True)
    need_cook= models.BooleanField(default=False,blank=True,null=True)
    need_driver = models.BooleanField(default=False,blank=True,null=True)
    is_paid = models.BooleanField(default=False,blank=True,null=True)
    booking_date = models.DateField(default=date.today)
    arrival_time = models.CharField(max_length=100,blank=True,null=True)
    reservation_from = models.CharField(max_length=100,blank=True,null=True)
# class Invoice(models.Model):
#     reservation_id = models.PositiveIntegerField()
#     booking_date = models.DateField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_paid = models.BooleanField(default=False)

class Review(models.Model):
    review = models.TextField()
    rating = models.PositiveIntegerField()
    user_name = models.CharField(max_length=100,blank=True,null=True)
    review_from = models.CharField(max_length=100,blank=True,null=True)