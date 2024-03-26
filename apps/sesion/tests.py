from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.urls import reverse
import json

def get_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class Test_Sesion(TestCase):
    print('TESTING SESION')
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testemail@gmail.com')
        self.client = APIClient()
        self.jwt_token = get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.jwt_token}')

    def test_login_success(self): 
        response = self.client.post(reverse('login'), data=json.dumps({'username': 'testuser', 'password': 'testpass'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertIn('access', response.json()['token'])

        
    def test_login_fail(self):
        response = self.client.post(reverse('login'), data=json.dumps({'username': 'testuser', 'password': 'wrongpass'}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Login fail'})
        
    def test_login_not_post_method(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 405)

