from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('api/<int:villa_id>/past_reservations/', views.get_past_reservations, name='past_reservations'),
    path('api/<int:villa_id>/ongoing_reservations/', views.get_ongoing_reservations, name='ongoing_reservations'),
    path('api/<int:villa_id>/upcoming_reservations/', views.get_upcoming_reservations, name='upcoming_reservations'),
    path('api/<int:villa_id>/availability/', views.get_villa_availability, name='villa_availability'),
    path('api/<int:villa_id>/check_availability/<str:check_in_date>/<str:check_out_date>/', views.check_villa_availability, name='check_availability'),
    path('api/reservations/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
    path('api/reservations/create/', views.create_reservation, name='create_reservation'),
    path('api/reservations/', views.get_all_reservations, name='all_reservations'),
]