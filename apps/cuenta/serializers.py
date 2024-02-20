from urllib import request
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
    propietario = serializers.CharField()
    
    def create(self, validated_data):
        print("LLega AAAAAAAAAAAAAAAAAAA")
        usuario_sesion = request.user
        perfil = Perfil.objects.get(user_id = usuario_sesion.id)
        
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(perfil.ci)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        
        return Response({"Cuenta creada"})
        # return Perfil.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.correo = validated_data.get('correo', instance.correo)
#         instance.telefono = validated_data.get('telefono', instance.telefono)
#         instance.direccion = validated_data.get('direccion', instance.direccion)
#         instance.sexo = validated_data.get('sexo', instance.sexo)
#         instance.contrasena = validated_data.get('contrasena', instance.contrasena)
#         instance.save()
        
#         return instance


# no_cuenta = models.TextField(max_length=16, unique=True, primary_key=True)
#     saldo = models.FloatField()
#     limite_ATM = models.IntegerField()
#     limite_POS = models.IntegerField()
#     tipo_cuenta = models.TextField(max_length=3)
#     propietario = models.ForeignKey(Perfil, on_delete=models.CASCADE)