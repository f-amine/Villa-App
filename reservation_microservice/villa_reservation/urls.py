from django.urls import path
from . import views

urlpatterns = [
    path('past_reservations/', views.get_past_reservations, name='past_reservations'),
    path('ongoing_reservations/', views.get_ongoing_reservations, name='ongoing_reservations'),
    path('upcoming_reservations/', views.get_upcoming_reservations, name='upcoming_reservations'),
    path('all_reservations/', views.get_all_reservations, name='all_reservations'),
    path('villa_availability/', views.get_villa_availability, name='villa_availability'),
    path('check_villa_availability/', views.check_villa_availability, name='check_villa_availability'),
    path('update_reservation/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
    path('create_reservation/', views.create_reservation, name='create_reservation'),
    path('sync_airbnb_calendar/', views.sync_airbnb_calendar, name='sync_airbnb_calendar'),
    path('generate_ical/', views.generate_ical, name='generate_ical'),
    path('user_reservations_byemail/<str:email>', views.get_user_reservations, name='user_reservations'),
    path('generate_receipt/<int:reservation_id>', views.generate_receipt, name='generate_reciept'),
    path('set_price/', views.set_price, name='set_price'),
    path('delete_reservation/<int:reservation_id>', views.delete_reservation, name='delete_reservation'),
]