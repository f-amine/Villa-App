# Generated by Django 4.2.4 on 2023-09-17 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villa_reservation', '0006_reservation_arrival_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('rating', models.PositiveIntegerField()),
                ('user_id', models.PositiveIntegerField()),
            ],
        ),
    ]
