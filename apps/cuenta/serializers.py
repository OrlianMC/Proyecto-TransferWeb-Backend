# from urllib import request
from rest_framework.response import Response
from rest_framework import serializers
from apps.usuario.models import Perfil
from apps.cuenta.models import Cuenta
from django.contrib.auth.models import User


class Cuenta_Serializer(serializers.Serializer):
    no_cuenta = serializers.CharField()
    saldo = serializers.FloatField()
    limite_ATM = serializers.IntegerField()
    limite_POS = serializers.IntegerField()
    tipo_cuenta = serializers.CharField(max_length=3)
    
    def create(self, validated_data):
        perfil_sesion = self.context['request'].user.perfil
        validated_data['propietario'] = perfil_sesion
        return Cuenta.objects.create(**validated_data)
    
    def update(self, cuenta, validated_data):
        cuenta.no_cuenta = validated_data.get('no_cuenta', cuenta.no_cuenta)
        cuenta.saldo = validated_data.get('saldo', cuenta.saldo)
        cuenta.limite_ATM = validated_data.get('limite_ATM', cuenta.limite_ATM)
        cuenta.limite_POS = validated_data.get('limite_POS', cuenta.limite_POS)
        cuenta.tipo_cuenta = validated_data.get('tipo_cuenta', cuenta.tipo_cuenta)
        cuenta.propietario = cuenta.propietario
        cuenta.save()
        
        return cuenta

class Listar_Cuenta_Serializer(serializers.Serializer):
    no_cuenta = serializers.CharField()
    saldo = serializers.FloatField()
    limite_ATM = serializers.IntegerField()
    limite_POS = serializers.IntegerField()
    tipo_cuenta = serializers.CharField(max_length=3)
    propietario = serializers.CharField()