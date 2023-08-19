import braintree
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import jwt
import requests
from rest_framework.decorators import api_view

@api_view(['POST'])
def checkout_page(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    print(user_id)
    #generate all other required data that you may need on the #checkout page and add them to context.
    reservation_id = request.data['reservation_id']
    reservation_response = requests.get(f'http://reservation-service:8080/reservation/get_reservation/{reservation_id}')
    reservation = reservation_response.json()
    if settings.BRAINTREE_PRODUCTION:
        braintree_env = braintree.Environment.Production
    else:
        braintree_env = braintree.Environment.Sandbox

    # Configure Braintree
    gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY
    )
    )
    try:
        client_token = gateway.client_token.generate({
            "customer_id": user_id
        })
    except:
        client_token = gateway.client_token.generate()

    context = {'braintree_client_token': client_token , 'reservation': reservation}
    return JsonResponse(context)

@api_view(['POST'])
def payment(request):
    nonce_from_the_client = request.POST['paymentMethodNonce']
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    user_response = requests.get(f'http://user-service:8000/users/api/user_by_id/{user_id}')
    user = user_response.json()
    customer_kwargs = {
        "first_name": user_response.json()['first_name'],
        "last_name": user_response.json()['last_name'],
        "email": user_response.json()['email'],
    }
    customer_create = braintree.Customer.create(customer_kwargs)
    customer_id = customer_create.customer.id
    result = braintree.Transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    return JsonResponse(result)
