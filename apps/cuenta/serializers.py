# from urllib import request
from rest_framework import serializers

# from apps.usuario.serializers import *
from apps.cuenta.models import Cuenta
      
class Cuenta_Serializer(serializers.ModelSerializer):
    propietario = serializers.CharField()
    
    class Meta:
        model = Cuenta
        fields = ['id', 'no_cuenta', 'saldo', 'limite_ATM', 'limite_POS', 'tipo_cuenta', 'nombre', 'propietario']