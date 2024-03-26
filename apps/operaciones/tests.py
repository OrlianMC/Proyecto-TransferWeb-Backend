import json
from django.contrib.auth.models import User
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
            saldo=1000.0,
            limite_ATM=500,
            limite_POS=1000,
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
        

# class Test_RealizarTransferencia(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.perfil = Perfil.objects.create(user=self.user)
#         self.cuenta_origen = Cuenta.objects.create(tipo_cuenta='tipo_cuenta', propietario=self.perfil, saldo=100.0, limite_ATM=200.0)
#         self.cuenta_destino = Cuenta.objects.create(tipo_cuenta='tipo_cuenta', propietario=self.perfil, saldo=0.0)
    
#     def test_realizar_transferencia(self):
#         request = self.factory.post('/realizar_transferencia', json.dumps({'monto': '50.0', 'moneda': 'tipo_cuenta', 'id': self.cuenta_origen.id, 'no_cuenta': self.cuenta_destino.no_cuenta}), content_type='application/json')
#         request.user = self.user
#         response = realizar_transferencia(request)
        
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data, {"message": "Transferencia completada, saldo restante: 50.0 tipo_cuenta"})
        
#         cuenta_origen = Cuenta.objects.get(id=self.cuenta_origen.id)
#         cuenta_destino = Cuenta.objects.get(no_cuenta=self.cuenta_destino.no_cuenta)
        
#         self.assertEqual(cuenta_origen.saldo, 50.0)
#         self.assertEqual(cuenta_destino.saldo, 50.0)
        
#         operaciones_origen = Operacion.objects.filter(cuenta=cuenta_origen)
#         self.assertEqual(operaciones_origen.count(), 1)
#         operacion_origen = operaciones_origen.first()
#         self.assertEqual(operacion_origen.informacion, str(cuenta_destino.no_cuenta))
#         self.assertEqual(operacion_origen.servicio, 'Transferencia')
#         self.assertEqual(operacion_origen.operacion, 'Débito')
#         self.assertEqual(operacion_origen.monto, 50.0)
#         self.assertEqual(operacion_origen.moneda, cuenta_origen.tipo_cuenta)
        
#         operaciones_destino = Operacion.objects.filter(cuenta=cuenta_destino)
#         self.assertEqual(operaciones_destino.count(), 1)
#         operacion_destino = operaciones_destino.first()
#         self.assertEqual(operacion_destino.servicio, 'Transferencia')
#         self.assertEqual(operacion_destino.operacion, 'Crédito')
#         self.assertEqual(operacion_destino.monto, 50.0)
#         self.assertEqual(operacion_destino.moneda, cuenta_destino.tipo_cuenta)

#         # Test para transferencia con cuenta de origen y destino que no coinciden con la moneda especificada
#         request_invalid = self.factory.post('/realizar_transferencia', json.dumps({'monto': '50.0', 'moneda': 'otra_moneda', 'id': self.cuenta_origen.id, 'no_cuenta': self.cuenta_destino.no_cuenta}), content_type='application/json')
#         request_invalid.user = self.user
#         response_invalid = realizar_transferencia(request_invalid)
        
#         self.assertEqual(response_invalid.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#         self.assertEqual(response_invalid.data, {"error": "Falló la transferencia, cuenta de origen y destino nocoinciden con la moneda especificada"})

#         # Test para transferencia con monto negativo
#         request_invalid = self.factory.post('/realizar_transferencia', json.dumps({'monto': '-50.0', 'moneda': 'tipo_cuenta', 'id': self.cuenta_origen.id, 'no_cuenta': self.cuenta_destino.no_cuenta}), content_type='application/json')
#         request_invalid.user = self.user
#         response_invalid = realizar_transferencia(request_invalid)
        
#         self.assertEqual(response_invalid.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#         self.assertEqual(response_invalid.data, {"error": "Monto no permitido"})

#         # Test para transferencia con monto que excede el límite ATM
#         request_invalid = self.factory.post('/realizar_transferencia', json.dumps({'monto': '250.0', 'moneda': 'tipo_cuenta', 'id': self.cuenta_origen.id, 'no_cuenta': self.cuenta_destino.no_cuenta}), content_type='application/json')
#         request_invalid.user = self.user
#         response_invalid = realizar_transferencia(request_invalid)
        
#         self.assertEqual(response_invalid.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#         self.assertEqual(response_invalid.data, {"error": "Monto excede el Limite ATM"})

#         # Test para transferencia con saldo insuficiente
#         request_invalid = self.factory.post('/realizar_transferencia', json.dumps({'monto': '150.0', 'moneda': 'tipo_cuenta', 'id': self.cuenta_origen.id, 'no_cuenta': self.cuenta_destino.no_cuenta}), content_type='application/json')
#         request_invalid.user = self.user
#         response_invalid = realizar_transferencia(request_invalid)
        
#         self.assertEqual(response_invalid.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#         self.assertEqual(response_invalid.data, {"error": "Saldo insuficiente"})