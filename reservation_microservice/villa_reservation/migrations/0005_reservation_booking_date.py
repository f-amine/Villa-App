# Generated by Django 4.2.4 on 2023-09-16 14:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villa_reservation', '0004_reservation_guest_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='booking_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]