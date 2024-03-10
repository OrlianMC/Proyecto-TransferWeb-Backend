import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.usuario.models import Perfil
from apps.cuenta.models import Cuenta
from apps.cuenta.serializers import *

@csrf_exempt
# @permission_classes([IsAuthenticated])
@api_view(['POST', 'PUT', 'DELETE', 'GET'])
def cuenta_gestionar(request):
    
    if request.method == 'GET':
        usuario = request.user
        propietario = Perfil.objects.get(user=1)  # Revisar si sirveeeeeeeeeeeeeeeeee
        cuenta = Cuenta.objects.filter(propietario=propietario)
        serializer = Cuenta_Serializer(cuenta, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        data_in = json.loads(request.body)
        
        usuario = request.user
        propietario = Perfil.objects.get(user=1)  # Revisar si sirveeeeeeeeeeeeeeeeee
        print(propietario)
        no_cuenta = data_in.get('no_cuenta')
        saldo = float(data_in.get('saldo'))
        limite_ATM = int(data_in.get('limite_ATM'))
        limite_POS = int(data_in.get('limite_POS'))
        tipo_cuenta = data_in.get('tipo_cuenta')
        nombre = data_in.get('nombre')
        
        validar_errores = validar_datos_cuenta(no_cuenta, saldo, limite_ATM, limite_POS, tipo_cuenta, nombre)
        if validar_errores:
            return Response({"error": "Datos incorrectos"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if propietario:
            existe = Cuenta.objects.filter(no_cuenta=no_cuenta).exists()
            if not existe:
                cuenta = Cuenta.objects.create(no_cuenta=no_cuenta, saldo=saldo, limite_ATM=limite_ATM, limite_POS=limite_POS, tipo_cuenta=tipo_cuenta, nombre=nombre, propietario=propietario)
                cuenta.save()
                return Response({"message": "Cuenta creada correctamente"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Cuenta existente"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    if request.method == "PUT":
        data_in = json.loads(request.body)
        cuenta_id = data_in.get('id')
        
        no_cuenta = data_in.get('no_cuenta')
        limite_ATM = int(data_in.get('limite_ATM'))
        limite_POS = int(data_in.get('limite_POS'))
        tipo_cuenta = data_in.get('tipo_cuenta')
        nombre = data_in.get('nombre')
        
        cuenta = get_object_or_404(Cuenta, id=cuenta_id)
        saldo = cuenta.saldo
        
        usuario = request.user
        propietario = Perfil.objects.get(user=1)  # Revisar si sirveeeeeeeeeeeeeeeeee
        if cuenta.propietario != propietario:
            return Response({"error": "Usted no tiene permiso para modificar esta cuenta"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        validar_errores = validar_datos_cuenta(no_cuenta, saldo, limite_ATM, limite_POS, tipo_cuenta, nombre)
        if validar_errores:
            return Response({"error": "Datos incorrectos"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        cuenta.no_cuenta = no_cuenta if no_cuenta else cuenta.no_cuenta
        cuenta.limite_ATM = limite_ATM if limite_ATM else cuenta.limite_ATM
        cuenta.limite_POS = limite_POS if limite_POS else cuenta.limite_POS
        cuenta.tipo_cuenta = tipo_cuenta if tipo_cuenta else cuenta.tipo_cuenta
        cuenta.nombre = nombre if nombre else cuenta.nombre
        
        cuenta.save()      
        return Response({"message": "Cuenta modificada correctamente"}, status=status.HTTP_201_CREATED)
    
    if request.method == 'DELETE':
        data_in = json.loads(request.body)
        cuenta_id = data_in.get('id')
        
        if cuenta_id is not None:
            cuenta = get_object_or_404(Cuenta, id=cuenta_id)
            if cuenta is not None:
                cuenta.delete()     
        return Response({"message": "Cuenta eliminada correctamente"}, status=status.HTTP_201_CREATED)
    
def validar_datos_cuenta(no_cuenta, saldo, limite_ATM, limite_POS, tipo_cuenta, nombre):
    errores = []
    
    if not all([no_cuenta, saldo, limite_ATM, limite_POS, tipo_cuenta, nombre]):
        errores.append("Faltan campos requeridos")
    
    if len(no_cuenta) > 16 | len(no_cuenta) < 16:
        errores.append("Número de cuenta incorrecto")
        
    if saldo < 0:
        errores.append("Saldo no permitido")
        
    if limite_ATM < 0 | limite_POS < 0:
        errores.append("Límite no permitido")
    
    if  len(tipo_cuenta) != 3:
        errores.append("Tipo de cuenta incorrecto")
    
    if len(nombre) > 100:
        errores.append("Nombre excede límite de 100 caracteres")
    
    return errores

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def cuenta_formulario(request): 
    data_in = json.loads(request.body)
    cuenta_id = data_in.get('id')
    cuenta = get_object_or_404(Cuenta, id=cuenta_id)
    serializer = Cuenta_Serializer(cuenta)
    return Response(serializer.data)
        

