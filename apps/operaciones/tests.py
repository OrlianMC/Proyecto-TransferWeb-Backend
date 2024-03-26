import json
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from apps.usuario.models import Perfil
from apps.cuenta.models import Cuenta
from apps.operaciones.models import Operacion
from .views import consultar_saldo, realizar_transferencia
from rest_framework.test import APIClient

class Test_ConsultarSaldo(TestCase):
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
        
        self.cuenta = Cuenta.objects.create(
            no_cuenta='1234567890123456',
            saldo=100000.0,
            limite_ATM=10000,
            limite_POS=10000,
            tipo_cuenta='CUP',
            propietario=self.perfil,
            nombre='Mi cuenta'
        )
    
    def test_consultar_saldo(self):
        url = reverse('consultar-saldo')
        self.client.force_authenticate(user=self.user)
        data = {'tipo_cuenta': 'CUP'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class Test_RealizarTransferencia(TestCase):
    print('TESTING REALIZAR TRANSFERENCIA')
    
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
        
        self.cuenta_origen = Cuenta.objects.create(
            no_cuenta='1234567890123456',
            saldo=1000.0,
            limite_ATM=100,
            limite_POS=100,
            tipo_cuenta='CUP',
            propietario=self.perfil,
            nombre='Mi cuenta 1'
        )
        self.cuenta_destino = Cuenta.objects.create(
            no_cuenta='1234567890123451',
            saldo=1000.0,
            limite_ATM=10000,
            limite_POS=10000,
            tipo_cuenta='CUP',
            propietario=self.perfil,
            nombre='Mi cuenta 2'
        )
    
    def test_realizar_transferencia(self):
        url = reverse('realizar-transferencia')   
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': '50',
            'moneda': 'CUP',
            'id': self.cuenta_origen.id,
            'no_cuenta': self.cuenta_destino.no_cuenta
            }
        response = self.client.post(url, data, format='json')
        
        cuenta_origen = get_object_or_404(Cuenta, id=self.cuenta_origen.id)
        cuenta_destino = get_object_or_404(Cuenta, no_cuenta=self.cuenta_destino.no_cuenta)
        
        self.assertEqual(cuenta_origen.saldo, 950.0)
        self.assertEqual(cuenta_destino.saldo, 1050.0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": "Transferencia completada, saldo restante: 950.0 CUP"})

        
        operaciones_origen = Operacion.objects.filter(cuenta=cuenta_origen)
        self.assertEqual(operaciones_origen.count(), 1)
        operacion_origen = operaciones_origen.first()
        self.assertEqual(operacion_origen.informacion, str(cuenta_destino.no_cuenta))
        self.assertEqual(operacion_origen.servicio, 'Transferencia')
        self.assertEqual(operacion_origen.operacion, 'Débito')
        self.assertEqual(operacion_origen.monto, 50.0)
        self.assertEqual(operacion_origen.moneda, cuenta_origen.tipo_cuenta)
        
        operaciones_destino = Operacion.objects.filter(cuenta=cuenta_destino)
        self.assertEqual(operaciones_destino.count(), 1)
        operacion_destino = operaciones_destino.first()
        self.assertEqual(operacion_destino.servicio, 'Transferencia')
        self.assertEqual(operacion_destino.operacion, 'Crédito')
        self.assertEqual(operacion_destino.monto, 50.0)
        self.assertEqual(operacion_destino.moneda, cuenta_destino.tipo_cuenta)

    def test_realizar_transferencia_distinta_moneda(self):
        url = reverse('realizar-transferencia')   
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': '50',
            'moneda': 'otra_moneda',
            'id': self.cuenta_origen.id,
            'no_cuenta': self.cuenta_destino.no_cuenta
            }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {"error": "Falló la transferencia, cuenta de origen y destino no coinciden con la moneda especificada"})
                
    def test_realizar_transferencia_monto_negativo(self):
        url = reverse('realizar-transferencia')   
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': '-50',
            'moneda': 'CUP',
            'id': self.cuenta_origen.id,
            'no_cuenta': self.cuenta_destino.no_cuenta
            }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {"error": "Monto no permitido"})
        
    def test_realizar_transferencia_excede_limite(self):
        url = reverse('realizar-transferencia')   
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': '150',
            'moneda': 'CUP',
            'id': self.cuenta_origen.id,
            'no_cuenta': self.cuenta_destino.no_cuenta
            }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {"error": "Monto excede el Limite ATM"})

    def test_realizar_transferencia_saldo_insuficiente(self):
        url = reverse('realizar-transferencia')   
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': '2000',
            'moneda': 'CUP',
            'id': self.cuenta_destino.id,
            'no_cuenta': self.cuenta_origen.no_cuenta
            }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {"error": "Saldo insuficiente"})
        
class Test_Recargar_Saldo_Movil(TestCase):
    print('TESTING RECAGAR MÓVIL')
      
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
        
        self.cuenta = Cuenta.objects.create(
            no_cuenta='1234567890123456',
            saldo=1000.0,
            limite_ATM=10000,
            limite_POS=10000,
            tipo_cuenta='CUP',
            propietario=self.perfil,
            nombre='Mi cuenta'
        )
        
    def test_recargar_saldo_movil(self):
        url = reverse('recargar-saldo-movil')
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': 250,
            'telefono': '58565408',
            'id': self.cuenta.id,
            'moneda': 'CUP'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    

        operaciones = Operacion.objects.filter(cuenta=self.cuenta)
        self.assertEqual(operaciones.count(), 1)
        operacion = operaciones.first()
        self.assertEqual(operacion.informacion, '58565408')
        self.assertEqual(operacion.servicio, 'Recarga Saldo Móvil')
        self.assertEqual(operacion.operacion, 'Débito')
        self.assertEqual(operacion.monto, 225.0)
        self.assertEqual(operacion.moneda, self.cuenta.tipo_cuenta)
        
    def test_recargar_saldo_movil_saldo_insuficiente(self):
        url = reverse('recargar-saldo-movil')
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': 2250,
            'telefono': '58565408',
            'id': self.cuenta.id,
            'moneda': 'CUP'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)    
        
    def test_recargar_saldo_movil_saldo_negativo(self):
        url = reverse('recargar-saldo-movil')
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': -250,
            'telefono': '58565408',
            'id': self.cuenta.id,
            'moneda': 'CUP'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
class Test_Recargar_Nauta(TestCase):
    print('TESTING RECAGAR NAUTA')
      
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
        
        self.cuenta = Cuenta.objects.create(
            no_cuenta='1234567890123456',
            saldo=1000.0,
            limite_ATM=10000,
            limite_POS=10000,
            tipo_cuenta='CUP',
            propietario=self.perfil,
            nombre='Mi cuenta'
        )
        
    def test_recargar_nauta(self):
        url = reverse('recargar-nauta')
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': 250,
            'telefono': '58565408',
            'id': self.cuenta.id,
            'tipo_cuenta': 'CUP',
            'nombre_usuario': 'testing'
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    

        operaciones = Operacion.objects.filter(cuenta=self.cuenta)
        self.assertEqual(operaciones.count(), 1)
        operacion = operaciones.first()
        self.assertEqual(operacion.informacion, 'testing')
        self.assertEqual(operacion.servicio, 'Recarga Nauta')
        self.assertEqual(operacion.operacion, 'Débito')
        self.assertEqual(operacion.monto, 225.0)
        self.assertEqual(operacion.moneda, self.cuenta.tipo_cuenta)
        
    def test_recargar_nauta_saldo_insuficiente(self):
        url = reverse('recargar-nauta')
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': 2500,
            'telefono': '58565408',
            'id': self.cuenta.id,
            'tipo_cuenta': 'CUP',
            'nombre_usuario': 'testing'
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)    
        
    def test_nauta_saldo_negativo(self):
        url = reverse('recargar-nauta')
        self.client.force_authenticate(user=self.user)
        data = {
            'monto': -250,
            'telefono': '58565408',
            'id': self.cuenta.id,
            'tipo_cuenta': 'CUP',
            'nombre_usuario': 'testing'
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)