# Generated by Django 4.2.4 on 2023-09-17 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villa_reservation', '0008_review_review_from'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user_id',
        ),
        migrations.AddField(
            model_name='review',
            name='user_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
