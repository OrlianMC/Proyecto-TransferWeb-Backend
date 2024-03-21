from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from apps.usuario.models import Perfil
from apps.cuenta.models import Cuenta

class CuentaGestionarViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.perfil = Perfil.objects.create(user=self.user)
        self.cuenta = Cuenta.objects.create(
            no_cuenta='1234567890123456',
            saldo=1000.0,
            limite_ATM=500,
            limite_POS=1000,
            tipo_cuenta='XYZ',
            propietario=self.perfil,
            nombre='Mi cuenta'
        )
    
    def test_get_cuentas(self):
        url = reverse('cuenta_gestionar')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Verifica que se devuelva una cuenta
    
    def test_create_cuenta(self):
        url = reverse('cuenta_gestionar')
        self.client.force_authenticate(user=self.user)
        data = {
            'no_cuenta': '9876543210987654',
            'saldo': 2000.0,
            'limite_ATM': 1000,
            'limite_POS': 2000,
            'tipo_cuenta': 'ABC',
            'nombre': 'Otra cuenta'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cuenta.objects.count(), 2)  # Verifica que se haya creado una nueva cuenta
    
    def test_create_existing_cuenta(self):
        url = reverse('cuenta_gestionar')
        self.client.force_authenticate(user=self.user)
        data = {
            'no_cuenta': '1234567890123456',  # Número de cuenta existente
            'saldo': 2000.0,
            'limite_ATM': 1000,
            'limite_POS': 2000,
            'tipo_cuenta': 'ABC',
            'nombre': 'Otra cuenta'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_cuenta(self):
        url = reverse('cuenta_gestionar')
        self.client.force_authenticate(user=self.user)
        data = {
            'id': self.cuenta.id,
            'no_cuenta': '9999999999999999',
            'limite_ATM': 700,
            'limite_POS': 1500,
            'tipo_cuenta': 'DEF',
            'nombre': 'Cuenta modificada'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta = Cuenta.objects.get(id=self.cuenta.id)
        self.assertEqual(cuenta.no_cuenta, '9999999999999999')
        self.assertEqual(cuenta.limite_ATM, 700)
        self.assertEqual(cuenta.limite_POS, 1500)
        self.assertEqual(cuenta.tipo_cuenta, 'DEF')
        self.assertEqual(cuenta.nombre, 'Cuenta modificada')
    
    def test_update_other_user_cuenta(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        other_perfil = Perfil.objects.create(user=other_user)
        other_cuenta = Cuenta.objects.create(
            no_cuenta='1111111111111111',
            saldo=2000.0,
            limite_ATM=500,
            limite_POS=1000,
            tipo_cuenta='XYZ',
            propietario=other_perfil,
            nombre='Otra cuenta'
        )
        url = reverse('cuenta_gestionar')
        self.client.force_authenticate(user=self.user)
        data = {
            'id': other_cuenta.id,
            'no_cuenta': '9999999999999999',
            'limite_ATM': 700,
            'limite_POS': 1500,
            'tipo_cuenta': 'DEF',
            'nombre': 'Cuenta modificada'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_delete_cuenta(self):
        url = reverse('cuenta_gestionar')
        self.client.force_authenticate(user=self.user)
        data = {
'id': self.cuenta.id
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cuenta.objects.count(), 0)  # Verifica que se haya eliminado la cuenta

class CuentaFormularioViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.perfil = Perfil.objects.create(user=self.user)
        self.cuenta = Cuenta.objects.create(
            no_cuenta='1234567890123456',
            saldo=1000.0,
            limite_ATM=500,
            limite_POS=1000,
            tipo_cuenta='XYZ',
            propietario=self.perfil,
            nombre='Mi cuenta'
        )
    
    def test_get_cuenta_formulario(self):
        url = reverse('cuenta_formulario')
        self.client.force_authenticate(user=self.user)
        data = {
            'id': self.cuenta.id
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['no_cuenta'], '1234567890123456')
        self.assertEqual(response.data['saldo'], 1000.0)
        self.assertEqual(response.data['limite_ATM'], 500)
        self.assertEqual(response.data['limite_POS'], 1000)
        self.assertEqual(response.data['tipo_cuenta'], 'XYZ')
        self.assertEqual(response.data['nombre'], 'Mi cuenta')