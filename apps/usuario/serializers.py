from rest_framework import serializers
from apps.usuario.models import Perfil
from django.contrib.auth.models import User

class Perfil_Serializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    telefono = serializers.CharField()
    direccion = serializers.CharField()
    ci = serializers.CharField()
    sexo = serializers.CharField()
    
    
    def create(self, validated_data):
        
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        # Crear un nuevo usuario en Django
        usuario = User.objects.create_user(username=username, email=email, password=password)

        telefono=validated_data.get('telefono')
        direccion=validated_data.get('direccion')
        ci=validated_data.get('ci')
        sexo=validated_data.get('sexo')
        
        return Perfil.objects.create(user=usuario, telefono=telefono, direccion=direccion, ci=ci, sexo=sexo)
    
    def update(self, perfil, validated_data):
    
        id_user = perfil.user.id
        usuario = User.objects.get(id=id_user)

        usuario.username = validated_data.get('username', usuario.username)
        usuario.email = validated_data.get('email', usuario.email)
        password = validated_data.get('password')
        if password is not None:
            usuario.set_password(password)
        usuario.save()
        
        # Campos del perfil que varian
        perfil.user = usuario
        perfil.telefono = validated_data.get('telefono', perfil.telefono)
        perfil.direccion = validated_data.get('direccion', perfil.direccion)
        perfil.sexo = validated_data.get('sexo', perfil.sexo)
        
        perfil.save()
        
        
        return perfil

class Perfil_Listar_Serializer(serializers.Serializer):
    user = serializers.CharField()
    telefono = serializers.CharField()
    direccion = serializers.CharField()
    ci = serializers.CharField()
    sexo = serializers.CharField()


# class Perfil_Serializer(serializers.Serializer):
#     correo = serializers.EmailField()
#     telefono = serializers.CharField()
#     direccion = serializers.CharField()
#     ci = serializers.CharField()
#     sexo = serializers.CharField()
#     contrasena = serializers.CharField()
    
#     def create(self, validated_data):
#         return Perfil.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.correo = validated_data.get('correo', instance.correo)
#         instance.telefono = validated_data.get('telefono', instance.telefono)
#         instance.direccion = validated_data.get('direccion', instance.direccion)
#         instance.sexo = validated_data.get('sexo', instance.sexo)
#         instance.contrasena = validated_data.get('contrasena', instance.contrasena)
#         instance.save()
        
#         return instance