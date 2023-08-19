from django.shortcuts import render
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
import jwt
import datetime


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return JsonResponse({'message': 'registered successfully', 'status': 200})
        else:
            print(serializer.errors)
            return JsonResponse({'message': 'Invalid Credentials', 'status': 401})
        

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        if not user.check_password(password):
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        payload = {
            'id': user.id,
            'superuser': user.is_superuser,
            'agent_id': user.agent_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':  datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'PLEASE WORK', algorithm='HS256').decode('utf-8')
        response = JsonResponse({'message': 'login successfully', 'status': 200})
        response.set_cookie('jwt', token)
        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        try:
            payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self,request):
        response =Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'Logged out Succesfully','status':200}
        return response
    

#get user by email
class GetUserByEmailView(APIView):
    def get(self, request, email):
        user = User.objects.filter(email=email).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
#get user by id
class GetUserByIdView(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)