# Generated by Django 4.2.4 on 2023-09-15 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
