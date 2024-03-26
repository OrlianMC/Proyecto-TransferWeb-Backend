from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.usuario.models import Perfil
from apps.servicio.models import Servicio
from django.contrib.auth.models import User

class Test_Servicio(TestCase):
    print('TESTING SERVICIO')
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testemail@test.com')
        self.perfil = Perfil.objects.create(
            user=self.user,
            direccion='testdireccion',
            telefono='12345678',
            ci='01010114524',
            sexo='M',
            email='testemail@test.com'
            )
        
        self.servicio = Servicio.objects.create(
            propietario=self.perfil,
            identificador='123',
            nombre='Servicio de prueba',
            campo='Campo de prueba',
            monto=10.0
        )
    
    def test_get_servicios(self):
        url = reverse('servicio-gestionar')
        self.client.force_authenticate(user=self.user) # force authenticated
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], self.servicio.nombre)
    
    def test_create_servicio(self):
        url = reverse('servicio-gestionar')
        self.user = User.objects.create_user(username='othertestuser', password='othertestpassword', email='othertestemail@test.com')
        self.perfil = Perfil.objects.create(
            user=self.user,
            direccion='othertestdireccion',
            telefono='12345600',
            ci='01010114500',
            sexo='M',
            email='othertestemail@test.com'
            )
        self.client.force_authenticate(user=self.user)
        data = {
            'propietario': self.perfil.id,
            'identificador': '456',
            'nombre': 'Nuevo servicio',
            'monto': 20.0,
            'campo': 'Campo de prueba'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Servicio.objects.count(), 2)
        # servicio_creado = Servicio.objects.get(identificador='456')
        # self.assertEqual(servicio_creado.nombre, 'Nuevo servicio')
    
    def test_update_servicio(self):
        url = reverse('servicio-gestionar')
        self.client.force_authenticate(user=self.user)
        data = {
            'id': self.servicio.id,
            'identificador': '123',
            'nombre': 'Servicio actualizado',
            'monto': 15.0,
            'campo': 'Campo actualizado'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        servicio_actualizado = Servicio.objects.get(id=self.servicio.id)
        self.assertEqual(servicio_actualizado.nombre, 'Servicio actualizado')
        self.assertEqual(servicio_actualizado.monto, 15.0)
        self.assertEqual(servicio_actualizado.campo, 'Campo actualizado')
    
    def test_delete_servicio(self):
        url = reverse('servicio-gestionar')
        self.client.force_authenticate(user=self.user)
        data = {
            'id': [self.servicio.id]
            }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Servicio.objects.count(), 0)