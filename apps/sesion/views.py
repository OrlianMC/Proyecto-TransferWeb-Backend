from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            serializer = MyTokenObtainPairSerializer(data=data)
            if serializer.is_valid():
                token = serializer.validated_data
                return JsonResponse({'token': token}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'message': 'Login fail'}, status=401)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)