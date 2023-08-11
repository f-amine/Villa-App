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
]