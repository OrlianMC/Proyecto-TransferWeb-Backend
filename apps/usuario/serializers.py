from rest_framework import serializers
from apps.usuario.models import Perfil
from django.contrib.auth.models import User

class PerfilSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model = Perfil
        fields = ['id','user', 'telefono', 'direccion', 'ci', 'sexo', 'email']