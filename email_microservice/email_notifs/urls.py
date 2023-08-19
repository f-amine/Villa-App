from django.urls import path
from .views import send_email,send_reminder_email

urlpatterns = [
    path('send_email/', send_email, name='send_email'),
    path('send_reminder/', send_reminder_email, name='send_reminder')
]