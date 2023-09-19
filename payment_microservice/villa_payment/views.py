import braintree
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import jwt
import requests
from rest_framework.decorators import api_view

@api_view(['POST'])
def checkout_page(request):
    token = request.data['jwt']
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    #generate all other required data that you may need on the #checkout page and add them to context.
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

    context = {'clientToken': client_token}
    
    return JsonResponse(context)

@api_view(['POST'])
def payment(request):
    gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY
    )
    )
    nonce_from_the_client = request.data['paymentMethodNonce']
    token = request.data['jwt']
    if not token:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    try:
        payload = jwt.decode(token, 'PLEASE WORK', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
    user_id = payload['id']
    user_response = requests.get(f'http://user-service:8000/users/api/user_by_id/{user_id}')
    user = user_response.json()
    braintree_id = user.get('braintree_id')
    if braintree_id:
        customer = gateway.customer.find(braintree_id)
    else:
        result = gateway.customer.create({
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email'],
        })
        braintree_id = result.customer.id
        requests.post(f'http://user-service:8000/users/api/update_user/{user_id}/', data={"braintree_id": braintree_id})
    payment_method = gateway.payment_method.create({
        "customer_id": braintree_id,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "make_default": True,
            "verify_card": True,
            "fail_on_duplicate_payment_method": True
            }
    })
    print(payment_method)
    amount = request.data['amount']
    result = gateway.transaction.sale({
        'amount': amount,
			'customer_id': braintree_id,
			'options': {
				"submit_for_settlement": True
			}
		})
    if result.is_success or result.transaction:
        return JsonResponse({
            "message": "Perfect",
            "tran_id": result.transaction.id,
        })
    else:
        return JsonResponse({
            "message": ", ".join([ f'{x.code} - {x.message}' for x in result.errors.deep_errors]),
            "tran_id": "N/A"
        })
