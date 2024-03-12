import json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.usuario.models import Perfil
from apps.cuenta.models import Cuenta
from apps.operaciones.models import Operacion
from apps.cuenta.serializers import *
from apps.operaciones.serializers import *
from datetime import datetime
from django.db.models import F

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def consultar_saldo(request):
    data_in = json.loads(request.body)
    tipo_cuenta = data_in.get('tipo_cuenta')
    usuario = request.user
    propietario = get_object_or_404(Perfil, user=usuario) #Cambiarrrrrrrrrrrrrrr
    cuentas = Cuenta.objects.filter(tipo_cuenta=tipo_cuenta, propietario=propietario)
    serializer = Cuenta_Serializer(cuentas, many=True)
    
    no_cuenta = []
    saldo = []
    mensaje = "Consulta de saldo completada: "

    for item in serializer.data:
        no_cuenta.append(item['no_cuenta'])
        saldo.append(item['saldo'])
        
    for i in range(len(no_cuenta)):
        mensaje += "Cuenta: " + str(no_cuenta[i]) + " Saldo: " + str(saldo[i]) +" "+ str(tipo_cuenta)+" "
    
    print(mensaje)
    return Response({"message": mensaje}, status=status.HTTP_201_CREATED)
    
@api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
def realizar_transferencia(request):
    if request.method == 'GET':
        usuario = 1 #request.user
        
        propietario = get_object_or_404(Perfil, user=usuario)
        cuenta = Cuenta.objects.filter(propietario=propietario)
        serializer = Cuenta_Serializer(cuenta, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        data_in = json.loads(request.body)
        monto = data_in.get('monto')
        moneda = data_in.get('moneda') #cuenta origen no cincide con la moneda especificada
        cuenta_id_origen = data_in.get('id')
        no_cuenta_destino = data_in.get('no_cuenta')
        
        cuenta_origen = get_object_or_404(Cuenta, id=cuenta_id_origen)
        cuenta_destino = get_object_or_404(Cuenta, no_cuenta=no_cuenta_destino)
        
        if cuenta_origen.tipo_cuenta != moneda or cuenta_destino.tipo_cuenta != moneda or cuenta_origen.tipo_cuenta != cuenta_destino.tipo_cuenta:
            return Response({"error": "Falló la transferencia, cuenta de origen y destino no coinciden con la moneda especificada"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if float(monto) < 0:
            return Response({"error": "Monto no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if float(monto) >  cuenta_origen.limite_ATM:
            return Response({"error": "Monto excede el Limite ATM"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if cuenta_origen.saldo >= float(monto):
            cuenta_origen.saldo -= float(monto)
            cuenta_origen.save()
            cuenta_destino.saldo += float(monto)
            cuenta_destino.save()
            
            # Agregar datos a la entidad operaciones para resumen de operaciones
            operacion_DB = Operacion.objects.create(cuenta=cuenta_origen, informacion=str(cuenta_destino.no_cuenta), servicio='Transferencia', operacion='Débito', monto=float(monto), moneda=cuenta_origen.tipo_cuenta)
            operacion_DB.save()
            operacion_CR = Operacion.objects.create(cuenta=cuenta_destino, servicio='Transferencia', operacion='Crédito', monto=float(monto), moneda=cuenta_destino.tipo_cuenta)
            operacion_CR.save()
            
        else:
            return Response({"error": "Saldo insuficiente"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        mensaje = "Transferencia completada, saldo restante: "+str(cuenta_origen.saldo)+" "+str(cuenta_origen.tipo_cuenta)
        
        return Response({"message": mensaje}, status=status.HTTP_201_CREATED)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def recargar_saldo_movil(request):
    if request.method == 'GET':
        usuario = request.user
        propietario = get_object_or_404(Perfil, user=usuario)  # Revisar si sirveeeeeeeeeeeeeeeeee
        cuenta = Cuenta.objects.filter(propietario=propietario)
        serializer = Cuenta_Serializer(cuenta, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        data_in = json.loads(request.body)
        monto = data_in.get('monto')
        telefono = data_in.get('telefono') 
        cuenta_id_origen = data_in.get('id')
        tipo_cuenta = data_in.get('tipo_cuenta')
        
        cuenta_origen = get_object_or_404(Cuenta, id=cuenta_id_origen, tipo_cuenta=tipo_cuenta)
        
        if float(monto) < 0:
            return Response({"error": "Monto no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if cuenta_origen.saldo >= float(monto):
            if tipo_cuenta == 'CUP':
                monto_new = float(monto) - float(monto)*0.1
                cuenta_origen.saldo -= monto_new
                cuenta_origen.save()
                mensaje = "La recarga se realizó con exito. Saldo a acreditar: "+str(monto)+" "+str(cuenta_origen.tipo_cuenta)+". Monto pagado: "+str(monto_new)+" "+str(cuenta_origen.tipo_cuenta)+". Teléfono: "+str(telefono)+". Saldo restante: "+str(cuenta_origen.saldo)+" "+str(cuenta_origen.tipo_cuenta)+". Gracias por utilizar nuestros servicios, ETECSA."
                operacion_DB = Operacion.objects.create(cuenta=cuenta_origen, informacion=str(telefono), servicio='Recarga Saldo Movil', operacion='Débito', monto=float(monto_new), moneda=cuenta_origen.tipo_cuenta)
                operacion_DB.save()
                
            if tipo_cuenta == 'MLC':
                monto_new = float(monto) - float(monto)*0.1
                cuenta_origen.saldo -= monto_new
                acreditado = float(monto)*24
                cuenta_origen.save()
                mensaje = "La recarga se realizó con exito. Saldo a acreditar: "+str(monto)+" "+str(cuenta_origen.tipo_cuenta)+". Monto pagado: "+str(monto_new)+" "+str(cuenta_origen.tipo_cuenta)+". Saldo acreditado: "+str(acreditado)+" CUP. Teléfono: "+str(telefono)+". Saldo restante: "+str(cuenta_origen.saldo)+" "+str(cuenta_origen.tipo_cuenta)+". Gracias por utilizar nuestros servicios, ETECSA."
                operacion_DB = Operacion.objects.create(cuenta=cuenta_origen,informacion=str(telefono), servicio='Recarga Saldo Movil', operacion='Débito', monto=float(monto_new), moneda=cuenta_origen.tipo_cuenta)
                operacion_DB.save()
        else:
            return Response({"error": "Saldo insuficiente"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response({"message": mensaje}, status=status.HTTP_201_CREATED)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def recargar_nauta(request):
    if request.method == 'GET':
        usuario = request.user
        propietario = get_object_or_404(Perfil, user=usuario)  # Revisar si sirveeeeeeeeeeeeeeeeee
        cuenta = Cuenta.objects.filter(propietario=propietario)
        serializer = Cuenta_Serializer(cuenta, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        data_in = json.loads(request.body)
        monto = data_in.get('monto')
        telefono = data_in.get('telefono') 
        cuenta_id_origen = data_in.get('id')
        tipo_cuenta = data_in.get('tipo_cuenta')
        nombre_usuario = data_in.get('nombre_usuario')
        
        cuenta_origen = get_object_or_404(Cuenta, id=cuenta_id_origen)
        
        if float(monto) < 0:
            return Response({"error": "Monto no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if cuenta_origen.saldo >= float(monto):
            if cuenta_origen.tipo_cuenta == 'CUP':
                monto_new = float(monto) - float(monto)*0.1
                cuenta_origen.saldo -= monto_new
                cuenta_origen.save()
                mensaje = "La recarga  nauta se realizó con exito. Saldo a acreditar: "+str(monto)+" "+str(cuenta_origen.tipo_cuenta)+". Monto pagado: "+str(monto_new)+" "+str(cuenta_origen.tipo_cuenta)+". Teléfono: "+str(telefono)+". Tipo de cuenta: "+str(tipo_cuenta)+". Nombre de usuario: "+str(nombre_usuario)+". Saldo restante: "+str(cuenta_origen.saldo)+" "+str(cuenta_origen.tipo_cuenta)+". Gracias por utilizar nuestros servicios, ETECSA."
                operacion_DB = Operacion.objects.create(cuenta=cuenta_origen,informacion=str(nombre_usuario), servicio='Recarga Nauta', operacion='Débito', monto=float(monto_new), moneda=cuenta_origen.tipo_cuenta)
                operacion_DB.save()
                
            if cuenta_origen.tipo_cuenta == 'MLC':
                monto_new = float(monto) - float(monto)*0.1
                cuenta_origen.saldo -= monto_new
                acreditado = float(monto)*24
                cuenta_origen.save()
                mensaje = "La recarga nauta se realizó con exito. Saldo a acreditar: "+str(monto)+" "+str(cuenta_origen.tipo_cuenta)+". Monto pagado: "+str(monto_new)+" "+str(cuenta_origen.tipo_cuenta)+". Saldo acreditado: "+str(acreditado)+" CUP. Teléfono: "+str(telefono)+". Tipo de cuenta: "+str(tipo_cuenta)+". Nombre de usuario: "+str(nombre_usuario)+". Saldo restante: "+str(cuenta_origen.saldo)+" "+str(cuenta_origen.tipo_cuenta)+". Gracias por utilizar nuestros servicios, ETECSA."
                operacion_DB = Operacion.objects.create(cuenta=cuenta_origen, informacion=str(nombre_usuario), servicio='Recarga Nauta', operacion='Débito', monto=float(monto_new), moneda=cuenta_origen.tipo_cuenta)
                operacion_DB.save()
        else:
            return Response({"error": "Saldo insuficiente"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response({"message": mensaje}, status=status.HTTP_201_CREATED)

@api_view(['POST', 'PUT', 'GET'])
@permission_classes([IsAuthenticated])
def limites(request):
    if request.method == 'GET':
        usuario = request.user
        propietario = get_object_or_404(Perfil, user=usuario)  # Revisar si sirveeeeeeeeeeeeeeeeee
        cuenta = Cuenta.objects.filter(propietario=propietario)
        serializer = Cuenta_Serializer(cuenta, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        data_in = json.loads(request.body)
        cuenta_id_origen = data_in.get('id')
        
        cuenta = get_object_or_404(Cuenta, id=cuenta_id_origen)
        
        limite_ATM = cuenta.limite_ATM
        limite_POS = cuenta.limite_POS
        
        mensaje = "Consulta de Límites de cuenta: "+str(cuenta.no_cuenta)+". Límite ATM: "+str(limite_ATM)+" .Límite POS: "+str(limite_POS)+"."
        return Response({"message": mensaje}, status=status.HTTP_201_CREATED)
    
    if request.method == "PUT":
        data_in = json.loads(request.body)
        cuenta_id_origen = data_in.get('id')
        limite_ATM_new = data_in.get('limite_ATM')
        limite_POS_new = data_in.get('limite_POS')
        
        cuenta = get_object_or_404(Cuenta, id=cuenta_id_origen)
        
        if int(limite_ATM_new) > 0 and int(limite_POS_new) > 0:
            cuenta.limite_ATM = limite_ATM_new
            cuenta.limite_POS = limite_POS_new
            cuenta.save()
            mensaje = "Cambio de límites efectuado correctamente."
            return Response({"message": mensaje}, status=status.HTTP_201_CREATED)
        return Response({"error": "Falló cambio de límites"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ultimas_operaciones(request):
    data_in = json.loads(request.body)
    cuenta_id_origen = data_in.get('id')
    tipo_servicio = data_in.get('tipo_servicio')
    
    # tipo_servicio = 'Todas las operaciones'
    # cuenta_id_origen = 1
    
    cuenta = get_object_or_404(Cuenta, id=cuenta_id_origen)
    
    if tipo_servicio != 'Todas las operaciones':
        operaciones = Operacion.objects.filter(cuenta=cuenta, servicio=tipo_servicio).order_by('-fecha')[:10]
    else:
        operaciones = Operacion.objects.filter(cuenta=cuenta).order_by('-fecha')[:10]
    
    serializer = Operaciones_Serializer(operaciones, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def detalle_operaciones(request):
    # data_in = json.loads(request.body)
    # cuenta_id_origen = data_in.get('id')
    
    cuenta_id_origen=5
    
    cuenta = get_object_or_404(Cuenta, id=cuenta_id_origen)
    
    operaciones = Operacion.objects.filter(cuenta=cuenta, operacion='Débito').order_by('-fecha')
    
    serializer = Operaciones_Serializer(operaciones, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def resumen_operaciones(request):
    # data_in = json.loads(request.body)
    # cuenta_id_origen = data_in.get('id')
    # mes_especifico = data_in.get('mes')
    # año_especifico = data_in.get('anio')
    # moneda = data_in.get('moneda')
    
    cuenta_id_origen=5
    mes_especifico = 3  # Por ejemplo, marzo
    año_especifico = 2024
    moneda = 'MLC'
    
    cuenta = get_object_or_404(Cuenta, id=cuenta_id_origen)
    
    # Obtén la fecha de inicio y fin del mes específico
    fecha_inicio = datetime(año_especifico, mes_especifico, 1)
    fecha_fin = datetime(año_especifico, mes_especifico + 1, 1)

    # Filtra las operaciones por cuenta, tipo de operación y fecha
    operaciones = Operacion.objects.filter(
        cuenta=cuenta,
        operacion='Débito',
        moneda=moneda,
        fecha__gte=fecha_inicio,
        fecha__lt=fecha_fin
    ).order_by('-fecha')
    
    suma = 0
    
    for item in operaciones:
        suma += float(item.monto)
    
    return Response(suma)