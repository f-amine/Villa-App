# Generated by Django 4.2.4 on 2023-09-17 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villa_reservation', '0005_reservation_booking_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='arrival_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
