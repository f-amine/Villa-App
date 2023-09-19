from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Reservation,DatePricing, Review
from .serializers import ReservationSerializer,DatePricingSerializer, ReviewSerializer
import jwt
import requests
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta,date
from icalendar import Calendar, Event
from django.http import HttpResponse
from rest_framework.decorators import api_view
import tempfile
from django.template.loader import render_to_string
from weasyprint import HTML

# Client Side apis 

#get past reservations
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
    reservations_data = [{'check_in_date': r.check_in_date, 'check_out_date': r.check_out_date, 'adult_numbers': r.adult_numbers, 'children_numbers': r.children_numbers, 'is_family': r.is_family} for r in past_reservations]
    return JsonResponse({'past reservations': reservations_data})


#get_upcoming_reservations

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
    reservations_data = [{'check_in_date': r.check_in_date, 'check_out_date': r.check_out_date, 'adult_numbers': r.adult_numbers, 'children_numbers': r.children_numbers, 'is_family': r.is_family} for r in upcoming_reservations]
    return JsonResponse({'upcoming reservations': reservations_data})

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
    reservations_data = [{'check_in_date': r.check_in_date, 'check_out_date': r.check_out_date, 'adult_numbers': r.adult_numbers, 'children_numbers': r.children_numbers, 'is_family': r.is_family} for r in ongoing_reservations]
    return JsonResponse({'ongoing reservations': reservations_data})
#get_reviews
@api_view(['GET'])
def get_reviews(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

# check_villa_availability
#http://example.com/get_villa_availability?check_in_date=2022-08-01&check_out_date=2022-08-10
@api_view(['POST'])
def check_villa_availability(request):
    check_in_date = request.data['check_in_date']
    check_out_date = request.data['check_out_date']
    if not check_in_date or not check_out_date:
        return JsonResponse({'message': 'Invalid request parameters', 'status': 400})
    try:
        check_in_date = date.fromisoformat(check_in_date)
        check_out_date = date.fromisoformat(check_out_date)
    except ValueError:
        return JsonResponse({'message': 'Invalid date format', 'status': 400})
    if check_in_date >= check_out_date:
        return JsonResponse({'message': 'Check-in date must be before check-out date', 'status': 400})
    if check_in_date < date.today():
        return JsonResponse({'message': 'Invalid date', 'status': 400})
    if Reservation.objects.filter(check_in_date__lt=check_out_date, check_out_date__gt=check_in_date).exists():
        return JsonResponse({'message': 'Villa is not available for the requested period', 'status': 400})
    return JsonResponse({'message': 'Villa is available for the requested period you can proceed to booking', 'status': 200})


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

@api_view(['POST'])
def create_reservation(request):
    if request.method == 'POST':
        check_in_date = request.data['check_in_date']
        check_out_date = request.data['check_out_date']
        token = request.data['jwt']
        #getting the user of the reservation
        if not token:
            return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
        try:
            payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
        #Checking Villa availability
        if not check_in_date or not check_out_date:
            return JsonResponse({'message': 'Invalid request parameters', 'status': 400})
        try:
            check_in_date = date.fromisoformat(check_in_date)
            check_out_date = date.fromisoformat(check_out_date)
        except ValueError:
            return JsonResponse({'message': 'Invalid date format', 'status': 400})
        if check_in_date >= check_out_date:
            return JsonResponse({'message': 'Check-in date must be before check-out date', 'status': 400})
        if check_in_date < date.today():
            return JsonResponse({'message': 'Invalid date', 'status': 400})
        if Reservation.objects.filter(check_in_date__lt=check_out_date, check_out_date__gt=check_in_date).exists():
            return JsonResponse({'message': 'Villa is not available for the requested period', 'status': 400})
        guest = payload['id']
        data = request.data.copy()
        data['user_id'] = guest
        #calculating the total price
        total_price = Decimal('0.00')
        current_date = check_in_date
        while current_date < check_out_date:
            try:
                date_pricing = DatePricing.objects.get(date=current_date)
                total_price += date_pricing.price
            except DatePricing.DoesNotExist:
                return JsonResponse({'message': f'No pricing information available for {current_date}', 'status': 400})
            current_date += timedelta(days=1)
        data['total_price'] = float(total_price)
        print(data)
        #creating the reservation
        serializer = ReservationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user_id=guest)
            response_data = {
                'reservation': serializer.data
            }
            return JsonResponse(response_data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
#get reservation price
@api_view(['POST'])
def get_reservation_price(request):
    if request.method == 'POST':
        check_in_date = request.data['check_in_date']
        check_out_date = request.data['check_out_date']
        #Checking Villa availability
        if not check_in_date or not check_out_date:
            return JsonResponse({'message': 'Invalid request parameters', 'status': 400})
        try:
            check_in_date = date.fromisoformat(check_in_date)
            check_out_date = date.fromisoformat(check_out_date)
        except ValueError:
            return JsonResponse({'message': 'Invalid date format', 'status': 400})
        if check_in_date >= check_out_date:
            return JsonResponse({'message': 'Check-in date must be before check-out date', 'status': 400})
        if check_in_date < date.today():
            return JsonResponse({'message': 'Invalid date', 'status': 400})
        if Reservation.objects.filter(check_in_date__lt=check_out_date, check_out_date__gt=check_in_date).exists():
            return JsonResponse({'message': 'Villa is not available for the requested period', 'status': 400})
        #calculating the total price
        total_price = Decimal('0.00')
        current_date = check_in_date
        while current_date < check_out_date:
            try:
                date_pricing = DatePricing.objects.get(date=current_date)
                total_price += date_pricing.price
            except DatePricing.DoesNotExist:
                return JsonResponse({'message': f'No pricing information available for {current_date}', 'status': 400})
            current_date += timedelta(days=1)
        return JsonResponse({'total_price': float(total_price)})
    

# _____________________________________________________________________________________________________________________________________
# admin side apis


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
        event = Event()
        event.add('summary', 'Reserved')
        event.add('dtstart', r.check_in_date)
        event.add('dtend', r.check_out_date)
        calendar.add_component(event)
    response = HttpResponse(calendar.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="calendar.ics"'
    return response

#getting the reservations of a user

@api_view(['GET'])
def get_user_reservations(request, email):
    if request.method == 'GET':
        user_response = requests.get(f'http://user-service:8000/users/api/user_by_email/{email}')
        if user_response.status_code == 200:
            user_id = user_response.json()['id']
            reservations = Reservation.objects.filter(user_id=user_id)
            serializer = ReservationSerializer(reservations, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'User not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

#getting the reservations of a user by id
@api_view(['POST'])
def get_user_reservations_by_cookie(request):
    token = request.data['jwt']
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    reservations = Reservation.objects.filter(user_id=user_id)
    reservations_data = []
    for reservation in reservations:
        check_in_date = reservation.check_in_date
        check_out_date = reservation.check_out_date
        total_price = Decimal('0.00')
        current_date = check_in_date
        while current_date < check_out_date:
            try:
                date_pricing = DatePricing.objects.get(date=current_date)
                total_price += date_pricing.price
            except DatePricing.DoesNotExist:
                return JsonResponse({'message': f'No pricing information available for {current_date}', 'status': 400})
            current_date += timedelta(days=1)
        reservation_data= {
            'reservation_id': reservation.id,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'adult_numbers': reservation.adult_numbers,
            'children_numbers': reservation.children_numbers,
            'is_family': reservation.is_family,
            'user_id': reservation.user_id,
            'is_paid': reservation.is_paid,
            'guest_country': reservation.guest_country,
            'guest_phone_number': reservation.guest_phone_number,
            'is_traveling_for_work': reservation.is_traveling_for_work,
            'need_cook': reservation.need_cook,
            'need_driver': reservation.need_driver,
            'total_paid': float(total_price),
            'arrival_time': reservation.arrival_time,
            "booking_date": reservation.booking_date,
            'reservation_from' : reservation.reservation_from
        }
        reservations_data.append(reservation_data)
    return JsonResponse({'reservations': reservations_data})

#generating a receipt as a pdf (untested)

@api_view(['GET'])
def generate_receipt(request, reservation_id):
    if request.method == 'GET':
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            print(reservation.user_id)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reservation not found.'}, status=404)
        user_response = requests.get(f'http://user-service:8000/users/api/user_by_id/{reservation.user_id}')
        if user_response.status_code == 200:
            user = user_response.json()
            html_string = render_to_string('receipt.html', {'reservation': reservation, 'user': user})
            html = HTML(string=html_string)
            result = html.write_pdf()
            response = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=reservation.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            return response
        else:
            return JsonResponse({'message': 'User not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



#set price for given dates 
@api_view(['POST'])
def set_price(request):
    if request.method == 'POST':
        token = request.data['jwt']
        if not token:
            return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
        try:
            payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
        if payload['superuser'] == False:
            return JsonResponse({'message': 'You are not authorized to perform this action', 'status': 401})
        data = request.data.copy()
        if not data['price']:
            return JsonResponse({'message': 'Invalid request parameters', 'status': 400})
        try:
            price = int(data['price'])
        except ValueError:
            return JsonResponse({'message': 'Invalid price', 'status': 400})
        if price < 0:
            return JsonResponse({'message': 'Invalid price', 'status': 400})
        start_date = date.fromisoformat(data['start_date'])
        end_date = date.fromisoformat(data['end_date'])
        if start_date >= end_date:
            return JsonResponse({'message': 'Start date must be before end date', 'status': 400})
        if start_date < date.today():
            return JsonResponse({'message': 'Invalid date', 'status': 400})
        for i in range((end_date - start_date).days+1):
            try:
                price = DatePricing.objects.get(date=start_date + timedelta(days=i))
                price.price = data['price']
                price.save()
            except DatePricing.DoesNotExist:
                price = DatePricing(date=start_date + timedelta(days=i), price=data['price'])
                price.save()
        return JsonResponse({'message': 'Price updated successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


#delete reservation
@api_view(['DELETE'])
def delete_reservation(request, reservation_id):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    if payload['superuser'] == False:
        return JsonResponse({'message': 'You are not authorized to perform this action', 'status': 401})
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.delete()
        return JsonResponse({'message': 'Reservation deleted successfully'}, status=200)
    except Reservation.DoesNotExist:
        return JsonResponse({'message': 'Reservation not found', 'status': 404})

#get_all_reservations
@api_view(['GET'])
def get_all_reservations(request):
    all_reservations = Reservation.objects.all()
    reservations_data = []
    for reservation in all_reservations:
        check_in_date = reservation.check_in_date
        check_out_date = reservation.check_out_date
        total_price = Decimal('0.00')
        current_date = check_in_date
        while current_date < check_out_date:
            try:
                date_pricing = DatePricing.objects.get(date=current_date)
                total_price += date_pricing.price
            except DatePricing.DoesNotExist:
                return JsonResponse({'message': f'No pricing information available for {current_date}', 'status': 400})
            current_date += timedelta(days=1)
        reservation_data= {
            'reservation_id': reservation.id,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'adult_numbers': reservation.adult_numbers,
            'children_numbers': reservation.children_numbers,
            'is_family': reservation.is_family,
            'user_id': reservation.user_id,
            'is_paid': reservation.is_paid,
            'guest_country': reservation.guest_country,
            'guest_phone_number': reservation.guest_phone_number,
            'is_traveling_for_work': reservation.is_traveling_for_work,
            'need_cook': reservation.need_cook,
            'need_driver': reservation.need_driver,
            'total_paid': float(total_price),
            'arrival_time': reservation.arrival_time,
            "booking_date": reservation.booking_date,
            'reservation_from' : reservation.reservation_from
        }
        reservations_data.append(reservation_data)
    return JsonResponse({'reservations': reservations_data})

#get_reservation_by_id
def get_reservation_by_id(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        check_in_date = reservation.check_in_date
        check_out_date = reservation.check_out_date
        total_price = Decimal('0.00')
        current_date = check_in_date
        while current_date < check_out_date:
            try:
                date_pricing = DatePricing.objects.get(date=current_date)
                total_price += date_pricing.price
            except DatePricing.DoesNotExist:
                return JsonResponse({'message': f'No pricing information available for {current_date}', 'status': 400})
            current_date += timedelta(days=1)
        reservation_data= {
            'reservation_id': reservation.id,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'adult_numbers': reservation.adult_numbers,
            'children_numbers': reservation.children_numbers,
            'is_family': reservation.is_family,
            'user_id': reservation.user_id,
            'is_paid': reservation.is_paid,
            'guest_country': reservation.guest_country,
            'guest_phone_number': reservation.guest_phone_number,
            'is_traveling_for_work': reservation.is_traveling_for_work,
            'need_cook': reservation.need_cook,
            'need_driver': reservation.need_driver,
            'total_paid': float(total_price),
            'arrival_time': reservation.arrival_time,
            "booking_date": reservation.booking_date,
            'reservation_from' : reservation.reservation_from
        }
        return JsonResponse(reservation_data)
    except Reservation.DoesNotExist:
        return JsonResponse({'message': 'Reservation not found', 'status': 404})
    
@api_view(['POST'])
def get_ical_events(request):
    ical_link = request.data['ical_link']
    if not ical_link:
        return JsonResponse({'error': 'No iCal link provided.'}, status=400)
    try:
        response = requests.get(ical_link)
        cal = Calendar.from_ical(response.text)
        events = []
        for event in cal.walk('VEVENT'):
            event_data = {
                'summary': event.get('summary'),
                'description': event.get('description'),
                'start_time': event.get('dtstart').dt.isoformat(),
                'end_time': event.get('dtend').dt.isoformat(),
                'location': event.get('location'),
            }
            events.append(event_data)
             # Create reservation for event if it doesn't exist already
            try:
                Reservation.objects.get(check_in_date=event_data['start_time'], check_out_date=event_data['end_time'])
            except Reservation.DoesNotExist:
                reservation_data = {
                    'user_id': 999,
                    'check_in_date': event_data['start_time'],
                    'check_out_date': event_data['end_time'],
                    'adult_numbers': 2,
                    'children_numbers': 0,
                    'is_paid': True,
                    'reservation_from': event_data['summary'],
                }
                reservation = Reservation.objects.create(**reservation_data)

        all_reservations = Reservation.objects.all()
        for reservationss in all_reservations:
            if reservationss.reservation_from == events[0]['summary']:
                # Check if reservation matches any of the events
                matches_event = False
                for event in events:
                    if reservationss.check_in_date == event['start_time'] and reservationss.check_out_date == event['end_time']:
                        matches_event = True
                        break
                # Delete reservation if it doesn't match any of the events
                if matches_event:
                    reservationss.delete()
        return JsonResponse({'events': events})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# all_reservations = Reservation.objects.all()
# for reservation in all_reservations:
#     if (reservation.reservation_from= "CLOSED - Not available" or reservation.reservation_from = "Airbnb (Not available)"):
#get nightly price for one year (each day)
@api_view(['GET'])
def get_nightly_price(request):
    if request.method == 'GET':
        start_date = date.today()
        end_date = start_date + timedelta(days=365)
        prices = DatePricing.objects.filter(date__gte=start_date, date__lte=end_date)
        serializer = DatePricingSerializer(prices, many=True)
        return JsonResponse({'nightly_price':serializer.data}, safe=False)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


#get_villa_availability
def get_villa_availability(request):
    today = date.today()
    available_dates = []
    for i in range(365 * 3):
        check_date = today + timedelta(days=i)
        if not Reservation.objects.filter(check_in_date__lte=check_date, check_out_date__gt=check_date).exists():
            available_dates.append(check_date.isoformat())
    return JsonResponse({'available_dates': available_dates})

#reads ical file and updates availability