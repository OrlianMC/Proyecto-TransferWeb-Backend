import json
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from apps.servicio.models import Servicio
from apps.usuario.models import Perfil
from apps.servicio.serializers import ServicioSerializer

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def gestionar_servicio(request):
    if request.method == 'GET':
        propietario = Perfil.objects.get(user=request.user)
        servicio = Servicio.objects.filter(propietario=propietario)
        serializer = ServicioSerializer(servicio, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data_in = json.loads(request.body)
        identificador = data_in.get('identificador')
        nombre = data_in.get('nombre')
        monto = data_in.get('monto')
        campo = "-"
        
        if nombre == "ONAT":
            campo = data_in.get('campo')    
        if nombre == "Multa de contravensión":
            campo = data_in.get('campo') 
        if nombre == "Multa de tránsito":
            campo = data_in.get('campo')     
            
        errores = validar_datos_servicio(monto, nombre, identificador, campo, True)
        
        if errores:
            mensajes = ""
            for error in errores:
                mensajes += error + " "
            return Response(mensajes)
        
        propietario = get_object_or_404(Perfil, user=request.user)
        servicio = Servicio.objects.create(propietario=propietario, nombre=nombre, identificador=identificador, monto=monto, campo=campo)
        servicio.save()
        return Response({"message": "Servicio creado correctamente"}, status=status.HTTP_201_CREATED)

    if request.method == 'PUT':
        data_in = json.loads(request.body)
        id = data_in.get('id')
        identificador = data_in.get('identificador')
        nombre = data_in.get('nombre')
        monto = data_in.get('monto')
        campo = data_in.get('campo')
        
        servicio_existente = get_object_or_404(Servicio, id=id)
        
        errores = validar_datos_servicio(monto, nombre, identificador, campo, False)
        
        if errores:
            mensajes = ""
            for error in errores:
                mensajes += error + " "
                return Response(mensajes)
            
        servicio_existente.nombre = nombre if nombre else servicio_existente.nombre
        servicio_existente.identificador = identificador if identificador else servicio_existente.identificador
        servicio_existente.monto = monto if monto else servicio_existente.monto
        servicio_existente.campo = campo if campo else servicio_existente.campo
        servicio_existente.save()
        
        return Response({"message": "Servicio modificado correctamente"}, status=status.HTTP_201_CREATED)
    
    if request.method == 'DELETE':
        data_in = json.loads(request.body)
        id = data_in.get('id')
        for item in id:
            servicio = get_object_or_404(Servicio, id=item)
            servicio.delete()
        return Response({"message": "Servicio eliminado correctamente"}, status=status.HTTP_200_OK)
       
       
def validar_datos_servicio(monto, nombre, identificador, campo, bandera):
    
    errores = []
    
    if not all([monto, identificador, nombre, campo]):
        errores.append("Faltan campos requeridos")
    
    if len(campo) > 150:
        errores.append("Campo excede límite de caracteres")
    
    if len(nombre) > 150:
        errores.append("Nombre excede límite de caracteres")
        
    if float(monto) < 0:
        errores.append("Monto no permitido")
    
    if(bandera == True):
        try:
            servicio = Servicio.objects.get(identificador=identificador)
            if servicio:
                errores.append("Identificador ya existe")
        except Servicio.DoesNotExist:
            pass  # No se encontró ningún servicio con el identificador, lo cual es válido
        except Exception as e:
            errores.append("Identificador ya existe")

    return errores    