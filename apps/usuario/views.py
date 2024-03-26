import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.usuario.models import Perfil
from apps.usuario.serializers import *
from django.views import View

@csrf_exempt
@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({"message": "Sesión cerrada correctamente"})

@api_view(['POST'])
def perfil_registrar(request):
            
    if request.method == 'POST':
        data_in = json.loads(request.body)
        
        username = data_in.get('username')   
        email = data_in.get('email')
        password = data_in.get('password')
        telefono=data_in.get('telefono')
        direccion=data_in.get('direccion')
        ci=data_in.get('ci')
        sexo=data_in.get('sexo')

        validar_errores = validar_datos_perfil(username, email, password, telefono, direccion, ci, sexo)
        if validar_errores:
            return Response({"error": "Datos incorrectos"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Crear un nuevo usuario en Django
        existe = User.objects.filter(username=username).exists()
        if not existe:
            usuario = User.objects.create_user(username=username, email=email, password=password)
            usuario.save()
        else:
            usuario = User.objects.get(username=username)

        perfil_existe = Perfil.objects.filter(user=usuario).exists()
        if not perfil_existe:
            perfil = Perfil.objects.create(user=usuario, telefono=telefono, direccion=direccion, ci=ci, sexo=sexo, email=email)
            perfil.save()
            return Response({"message": "Perfil creado correctamente"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Este usuario ya se encuentra registrado"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['PUT', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def perfil_administrar(request):
    
    if request.method == 'GET':
        perfil = Perfil.objects.all()
        serializer = PerfilSerializer(perfil, many=True)
        return Response(serializer.data)  
      
    if request.method == "PUT":
        data_in = json.loads(request.body)
        perfil_id = data_in.get('id')
        
        username = data_in.get('username')   
        email = data_in.get('email')
        password = data_in.get('password')
        telefono=data_in.get('telefono')
        direccion=data_in.get('direccion')
        ci=data_in.get('ci')
        sexo=data_in.get('sexo')
        
        perfil = get_object_or_404(Perfil, id=perfil_id)
        
        usuario_logueado = request.user
        propietario = Perfil.objects.get(user=usuario_logueado)  # Revisar si sirveeeeeeeeeeeeeeeeee
        if perfil.user != usuario_logueado:
            return Response({"error": "Usted no tiene permiso para modificar este perfil"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        validar_errores = validar_datos_perfil(username, email, password, telefono, direccion, ci, sexo)
        if validar_errores:
            return Response({"error": "Datos incorrectos"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        id_user = perfil.user.id
        usuario = User.objects.get(id=id_user)
        
        usuario.username = username if username else usuario.username
        usuario.email = email if email else usuario.email
        usuario.set_password(password)
        usuario.save()
        
        perfil.email = email if email else perfil.email
        perfil.telefono = telefono if telefono else perfil.telefono
        perfil.direccion = direccion if direccion else perfil.direccion
        perfil.ci = ci if ci else perfil.ci
        perfil.sexo = sexo if sexo else perfil.sexo
        perfil.save()       

        return Response({"message": "Perfil modificado correctamente"}, status=status.HTTP_201_CREATED)
    
    if request.method == 'DELETE':
        usuario_autenticado = request.user
        # usuario_autenticado = 'titotitotito'
        print(usuario_autenticado)
        usuario = User.objects.get(username=usuario_autenticado.username)    # Cambiarrrrrrrr
        usuario.delete()
        return Response({"message": "Perfil eliminado correctamente"}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_formulario(request):
    usuario = request.user
    perfil = Perfil.objects.get(user=usuario)
    serializer = PerfilSerializer(perfil)
    return Response(serializer.data)
    
def validar_datos_perfil(username, email, password, telefono, direccion, ci, sexo):
    errores = []
    
    if not all([username, email, password, telefono, direccion, ci, sexo]):
        errores.append("Faltan campos requeridos")
    
    if len(username) > 100:
        errores.append("Nombre de usuario excede límite de 100 caracteres")
        
    if len(direccion) > 250:
        errores.append("Nombre de usuario excede límite de 100 caracteres")
        
    if len(sexo) != 1:
        errores.append("Sexo excede límite de 1 caracter")
    
    if  len(telefono) != 8:
        errores.append("Número de telefono incorrecto")
    
    if len(password) < 8:
        errores.append("Contraseña tiene menos de 8 caracteres")
        
    try:
        # Validar la longitud de la cadena
        if len(ci) != 11:
            errores.append("Carnet de identidad incorrecto")

        # Extraer los componentes de la fecha
        anio = ci[:2]
        mes = ci[2:4]
        dia = ci[4:6]

        # Validar los componentes de la fecha
        if not (1 <= int(mes) <= 12):
            errores.append("El mes debe estar entre 1 y 12")
        if not (1 <= int(dia) <= 31):
            errores.append("El día debe estar entre 1 y 31")

    except Exception as e:
        # Manejar la excepción
        return Response("Error al validar la fecha: {}".format(str(e)))
    
    return errores