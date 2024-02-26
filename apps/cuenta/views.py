import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.usuario.models import Perfil
from apps.cuenta.models import Cuenta
from apps.cuenta.serializers import Cuenta_Serializer

@csrf_exempt
# @login_required
@api_view(['POST', 'PUT', 'DELETE'])
def cuenta_registrar(request):
    if request.method == 'POST':
        usuario_sesion = request.user
        usuario_id = usuario_sesion.id
        print(usuario_sesion)
        print(usuario_id)
        de_serializer = Cuenta_Serializer(data=request.data, context={'request': request})
        if de_serializer.is_valid():
            de_serializer.save()
            return Response({"message": "Cuenta creada correctamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if request.method == "PUT":
            
        data_in = json.loads(request.body)
        no_cuenta = data_in.get('no_cuenta')
        
        if no_cuenta is not None:
            cuenta = Cuenta.objects.get(no_cuenta=no_cuenta)             
            if cuenta is not None:             
                de_serializer = Cuenta_Serializer(cuenta, data=request.data)
                if de_serializer.is_valid():
                    de_serializer.save()     
                    return Response({"Cuenta modificada"})
                
        return Response(de_serializer.errors)
    
    if request.method == 'DELETE':
        data_in = json.loads(request.body)
        no_cuenta = data_in.get('no_cuenta')
        if no_cuenta is not None:
            cuenta = Cuenta.objects.get(no_cuenta=no_cuenta)  
            if cuenta is not None:
                cuenta.delete()     
        return Response({"Cuenta eliminada"})