from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Reservation
import jwt
import requests
from django.http import JsonResponse
from datetime import datetime, timedelta,date
from icalendar import Calendar, Event
from django.http import HttpResponse


def get_past_reservations(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    past_reservations = Reservation.objects.filter(user_id=user_id, check_out_date__lt=date.today())
    reservations_data = [{'check_in_date': r.check_in_date, 'check_out_date': r.check_out_date, 'guest_numbers': r.guest_numbers, 'is_family': r.is_family} for r in past_reservations]
    return JsonResponse({'reservations': reservations_data})
#get_ongoing_reservations

def get_ongoing_reservations(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    ongoing_reservations = Reservation.objects.filter(user_id=user_id, check_in_date__lte=date.today(), check_out_date__gte=date.today())
    reservations_data = [{'check_in_date': r.check_in_date, 'check_out_date': r.check_out_date, 'guest_numbers': r.guest_numbers, 'is_family': r.is_family} for r in ongoing_reservations]
    return JsonResponse({'reservations': reservations_data})

# get_upcoming_reservations
def get_upcoming_reservations(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    upcoming_reservations = Reservation.objects.filter(user_id=user_id, check_in_date__gt=date.today())
    reservations_data = [{'check_in_date': r.check_in_date, 'check_out_date': r.check_out_date, 'guest_numbers': r.guest_numbers, 'is_family': r.is_family} for r in upcoming_reservations]
    return JsonResponse({'reservations': reservations_data})
#get_all_reservations
def get_all_reservations(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    all_reservations = Reservation.objects.filter(user_id=user_id)
    reservations_data = [{'check_in_date': r.check_in_date, 'check_out_date': r.check_out_date, 'guest_numbers': r.guest_numbers, 'is_family': r.is_family} for r in all_reservations]
    return JsonResponse({'reservations': reservations_data})

#get_villa_availability

def get_villa_availability(request):
    today = date.today()
    available_dates = []
    for i in range(365 * 3):
        check_date = today + timedelta(days=i)
        if not Reservation.objects.filter(check_in_date__lte=check_date, check_out_date__gt=check_date).exists():
            available_dates.append(check_date.isoformat())
    return JsonResponse({'available_dates': available_dates})

# check_villa_availability
#http://example.com/get_villa_availability?check_in_date=2022-08-01&check_out_date=2022-08-10
def check_villa_availability(request):
    check_in_date = request.GET.get('check_in_date')
    check_out_date = request.GET.get('check_out_date')
    if not check_in_date or not check_out_date:
        return JsonResponse({'message': 'Invalid request parameters', 'status': 400})
    try:
        check_in_date = date.fromisoformat(check_in_date)
        check_out_date = date.fromisoformat(check_out_date)
    except ValueError:
        return JsonResponse({'message': 'Invalid date format', 'status': 400})
    if check_in_date >= check_out_date:
        return JsonResponse({'message': 'Check-in date must be before check-out date', 'status': 400})
    if Reservation.objects.filter(check_in_date__lt=check_out_date, check_out_date__gt=check_in_date).exists():
        return JsonResponse({'message': 'Villa is not available for the requested period', 'status': 400})
    return JsonResponse({'message': 'Villa is available for the requested period', 'status': 200})


def update_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation not found.'}, status=404)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reservation.check_in_date = start_date
        reservation.check_out_date = end_date
        
        reservation.save()

        data = serializers.serialize('json', [reservation])
        return JsonResponse(data, safe=False, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



def create_reservation(request):
    if request.method == 'POST':

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        guest_numbers = request.POST.get('guest_numbers')
        is_family = request.POST.get('is_family')
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
        try:
            payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
        user_id = payload['id']
        reservation = Reservation(check_in_date=start_date, check_out_date=end_date, guest=user_id, guest_numbers=guest_numbers, is_family=is_family)
        reservation.save()

        data = serializers.serialize('json', [reservation])
        return JsonResponse(data, safe=False, status=201)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

#syncs airbnb calendar with our calendar
def sync_airbnb_calendar(request):
    airbnb_calendar_url = 'https://www.airbnb.com/calendar/ical/123456.ics'  # Replace with your Airbnb iCal URL
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=365)
    reservations = Reservation.objects.filter(check_in_date__gte=start_date, check_out_date__lte=end_date)
    calendar_data = []
    for r in reservations:
        for i in range((r.check_out_date - r.check_in_date).days):
            event = Event()
            event.add('summary', 'Reserved')
            event.add('dtstart', r.check_in_date + timedelta(days=i))
            event.add('dtend', r.check_in_date + timedelta(days=i+1))
            calendar_data.append(event)
    headers = {'Content-Type': 'text/calendar'}
    response = requests.put(airbnb_calendar_url, headers=headers, data=Calendar(calendar_data).to_ical())
    if response.status_code == 200:
        return JsonResponse({'message': 'Calendar synced successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Failed to sync calendar'}, status=500)


#generates ical file

def generate_ical(request):
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=365)
    reservations = Reservation.objects.filter(check_in_date__gte=start_date, check_out_date__lte=end_date)
    calendar = Calendar()
    for r in reservations:
        for i in range((r.check_out_date - r.check_in_date).days):
            event = Event()
            event.add('summary', 'Reserved')
            event.add('dtstart', r.check_in_date + timedelta(days=i))
            event.add('dtend', r.check_in_date + timedelta(days=i+1))
            calendar.add_component(event)
    response = HttpResponse(calendar.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="calendar.ics"'
    return response