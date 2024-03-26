from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.usuario.models import Perfil


class Test_Perfil(TestCase):
    print("TESTING PERFIL")
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.perfil = Perfil.objects.create(
            user=self.user,
            telefono='12345678',
            direccion='Dirección de prueba',
            ci='12345678901',
            sexo='M', 
            email='test@example.com')

    def test_perfil_registrar(self):
        url = reverse('usuarios-registrar')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'telefono': '87654321',
            'direccion': 'Otra dirección de prueba',
            'ci': '02020232109',
            'sexo': 'F'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Perfil.objects.count(), 2)
        self.assertEqual(User.objects.count(), 2)

    def test_perfil_registrar_usuario_existente(self):
        url = reverse('usuarios-registrar')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'newpassword',
            'telefono': '87654321',
            'direccion': 'Otra dirección de prueba',
            'ci': '05050532109',
            'sexo': 'F'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['error'], 'Este usuario ya se encuentra registrado')

    def test_perfil_administrar_get(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('usuarios-modificar')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['telefono'], '12345678')

    def test_perfil_administrar_put(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('usuarios-modificar')
        data = {
            'id': self.perfil.id,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'newpassword',
            'telefono': '87654321',
            'direccion': 'Otra dirección de prueba',
            'ci': '05050532109',
            'sexo': 'F'
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.perfil.refresh_from_db()
        self.assertEqual(self.perfil.telefono, '87654321')
        self.assertEqual(self.perfil.direccion, 'Otra dirección de prueba')

    def test_perfil_administrar_put_no_permiso(self):
        user2 = User.objects.create_user(username='testuser2', password='testpassword')
        perfil2 = Perfil.objects.create(user=user2, telefono='11111111', direccion='Dirección de prueba 2',
                                        ci='11111111111', sexo='F', email='test2@example.com')

        self.client.force_authenticate(user=user2)
        url = reverse('usuarios-modificar')
        data = {
            'id': self.perfil.id,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'newpassword',
            'telefono': '87654321',
            'direccion': 'Otra dirección de prueba',
            'ci': '05050832109',
            'sexo': 'F'
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['error'], 'Usted no tiene permiso para modificar este perfil')

    def test_perfil_administrar_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('usuarios-modificar')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertFalse(Perfil.objects.filter(user=self.user).exists())

    def test_perfil_formulario(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('cargar-usuario-formulario')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['telefono'])prin