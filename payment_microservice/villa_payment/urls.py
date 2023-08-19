from django.urls import path
from . import views

urlpatterns = [
    path('checkout_page/', views.checkout_page, name='checkout_page'),
    path('payment/', views.payment, name='payment'),
]