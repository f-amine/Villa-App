from datetime import date, datetime, timedelta
import json
from django.conf import settings
from django.http import JsonResponse
import jwt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import requests

# Send reservation confirmation email

@api_view(['POST'])
def send_email(request):
    if not request.data:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    user_response = requests.get(f'http://user-service:8000/users/api/user_by_id/{user_id}')
    if user_response.status_code == 200:
        data = {
            'reservation_data': request.data,
            'user_data': user_response.json()
        }
        html_body = render_to_string("email_template.html", data)
        msg = EmailMultiAlternatives(
            subject="Villa Chouiter Center Reservation Confirmation",
            from_email=settings.EMAIL_HOST_USER,
            to=[user_response.json()['email']],
            cc=['friradriss57@gmail.com'],
            body=html_body)
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        return Response({'message': 'Email sent successfully', 'status': 200, 'data': data})
    else:
        return JsonResponse({'message': 'User not found.'}, status=404)

@api_view(['POST'])
def send_reminder_email(request):
    reservation_response = requests.get(f'http://reservation-service:8080/reservation/all_reservations/')
    if reservation_response.status_code == 200:
        reservations = reservation_response.json()
        for reservation in reservations["reservations"]:
            check_in_date = datetime.strptime(reservation['check_in_date'], '%Y-%m-%d').date()
            tomorrow = date.today() + timedelta(days=1)
            if check_in_date == tomorrow:
                guest_response = requests.get(f'http://user-service:8000/users/api/user_by_id/{reservation["user_id"]}')
                if guest_response.status_code == 200:
                    guest_data = guest_response.json()
                    data = {
                        'reservation_data': reservation,
                        'guest_data': guest_data
                    }
                    html_body = render_to_string("reminder_email_template.html", data)
                    msg = EmailMultiAlternatives(
                        subject="Villa Chouiter Center Reservation Reminder",
                        from_email=settings.EMAIL_HOST_USER,
                        to=[guest_data['email']],
                        cc=['friradriss57@gmail.com'],
                        body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
        return Response({'message': 'Reminder emails sent successfully', 'status': 200})
    else:
        return JsonResponse({'message': 'Error retrieving reservations.'}, status=500)