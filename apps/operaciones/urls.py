from django.urls import path
from apps.operaciones.views import *

urlpatterns = [
    path('saldo/', consultar_saldo, name='consultar-saldo'),
    path('transferencia/', realizar_transferencia, name='realizar-transferencia'),
    path('recargarMovil/', recargar_saldo_movil, name='recargar-saldo-movil'),
    path('recargarNauta/', recargar_nauta, name='recargar-nauta'),
    path('ultimasOperaciones/', ultimas_operaciones, name='ultimas-operaciones'),
    path('detalleOperaciones/', detalle_operaciones, name='detalle-operaciones'),
    path('resumenOperaciones/', resumen_operaciones, name='resumen-operaciones'),
    path('consultarServicio/', consultar_servicio, name='consultar-factura'),
    path('pagarServicio/', pagar_servicio, name='pagar-factura'),
    path('limites/', limites, name='limites'),
]

#http://127.0.0.1:8000/operaciones/