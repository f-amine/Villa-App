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
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    adult_numbers = models.PositiveIntegerField()
    children_numbers = models.PositiveIntegerField()
    is_family = models.BooleanField(default=True)
    user_id = models.PositiveIntegerField()
    