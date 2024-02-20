import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.usuario.models import Perfil
from apps.usuario.serializers import Perfil_Serializer, Perfil_Listar_Serializer

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({True})

        
    return Response({False})

@csrf_exempt
@api_view()
def logout_user(request):
    logout(request)
    return Response({"Sesión cerrada correctamente"})

@csrf_exempt
@api_view(['POST'])
def usuarios_registrar(request):
    if request.method == 'POST':
        de_serializer = Perfil_Serializer(data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response({"message": "Perfil creado correctamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@login_required
@api_view(['PUT', 'GET', 'DELETE'])
def usuarios_modificar(request):
    if request.method == 'GET': 
        perfil = Perfil.objects.all()
        serializer = Perfil_Listar_Serializer(perfil, many = True)
        return Response(serializer.data)

    if request.method == 'PUT':
        
        data_in = json.loads(request.body)
        perfil_id = data_in.get('ci')
        
        if perfil_id is not None:
            perfil = Perfil.objects.get(ci=perfil_id)
                            
            if perfil is not None:             
                de_serializer = Perfil_Serializer(perfil, data=request.data)
                if de_serializer.is_valid():
                    de_serializer.save()     
                    return Response({"Usuario modificado"})
                
        return Response(de_serializer.errors)
    
    if request.method == 'DELETE':
        usuario_sesion = request.user
        usuario_sesion.delete()
        return Response({"Usuario eliminado"})

# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def usuarios_administrar(request):
#     if request.method == 'GET': 
#         usuario = Perfil.objects.all()
#         serializer = Perfil_Serializer(usuario, many = True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         de_serializer = Perfil_Serializer(data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors)
    
#     if request.method == 'PUT':
#         data_in = json.loads(request.body)
#         usuario_id = data_in.get('ci')
#         if usuario_id is not None:
#             usuario = Perfil.objects.get(ci=usuario_id)
#             if usuario is not None:             
#                 de_serializer = Perfil_Serializer(usuario, data=request.data)
#                 if de_serializer.is_valid():
#                     de_serializer.save()     
#                     return Response(de_serializer.data)
#         return Response(de_serializer.errors)
    
@api_view()
def cargar_usuario_formulario(request):
    if request.method == 'GET': 
        data_in = json.loads(request.body)
        usuario_id = data_in.get('ci')
        if usuario_id is not None:
            usuario = Perfil.objects.get(ci=usuario_id)
            if usuario is not None:
                serializer = Perfil_Serializer(usuario)
            return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def buscar_usuario(request):
    
    if request.method == 'POST':
        
        data = json.loads(request.body)
        correo = data.get('correo')
        contrasena = data.get('contrasena')    
                      
        usuario_encontrado = Perfil.objects.filter(correo=correo, contrasena = contrasena).first()
        
        if usuario_encontrado:
            return HttpResponse("Usuario encontrado: " + usuario_encontrado.correo)
        else:
            return HttpResponse("Usuario no encontrado")    
    else:
        return HttpResponse("Método no permitido")
