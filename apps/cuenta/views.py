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
@api_view(['POST'])
def cuenta_registrar(request):
    if request.method == 'POST':
        de_serializer = Cuenta_Serializer(data=request.data)
        if de_serializer.is_valid():
            print("ENtraaaaaaaaaaaaaaaaaaaaaa")
            de_serializer.save()
            return Response({"message": "Cuenta creada correctamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)