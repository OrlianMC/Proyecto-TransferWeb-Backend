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
            print(request.COOKIES)
            print(request.user)
            return Response({True})

        
    return Response({False})

@csrf_exempt
@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({"message": "Sesión cerrada correctamente"})

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
@api_view(['PUT', 'GET', 'POST'])
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

@csrf_exempt
@api_view(['POST'])
def usuarios_eliminar(request):
    
    data_in = json.loads(request.body)
    username = data_in.get('username')
    
    try:
        usuario = User.objects.get(username=username)
        usuario.delete()
        return Response({"message": "Usuario eliminado"})
    except User.DoesNotExist:
        return Response({"error": "El usuario no existe"})       
        
    return Response({"Usuario eliminado"})

@csrf_exempt
@api_view(['POST'])
def cargar_usuario_formulario(request):
    
    data_in = json.loads(request.body)
    username = data_in.get('username')
        
    if username is not None:
        usuario = User.objects.get(username=username)
            
        try:
            perfil = Perfil.objects.get(user=usuario.id)
            serializer = Perfil_Listar_Serializer(perfil)
            return Response(serializer.data)
        except Perfil.DoesNotExist:
            return Response({"error": "El perfil del usuario no existe."}, status=404)
    else:
        return Response({"error": "No se encontró un usuario autenticado."}, status=401)
