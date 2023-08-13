from django.db import models

# Create your models here.

class Email(models.Model):
    to = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    reservation_id = models.IntegerField()