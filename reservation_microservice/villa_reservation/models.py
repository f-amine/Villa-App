from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.conf import settings

class Availability(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()


class Reservation(models.Model):
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guest_numbers = models.PositiveIntegerField()
    is_family = models.BooleanField(default=True)
    user_id = models.PositiveIntegerField()
    