from rest_framework import serializers
from apps.operaciones.models import Operacion
      
class Operaciones_Serializer(serializers.ModelSerializer):    
    class Meta:
        model = Operacion
        fields = ['informacion', 'fecha', 'servicio', 'operacion', 'monto', 'moneda']