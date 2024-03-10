from django.urls import path, include
from apps.cuenta.views import *

urlpatterns = [
    path('registrar/', cuenta_gestionar, name='cuenta-registrar'),
    path('formulario/', cuenta_formulario, name='cuenta-formulario'),
]

#http://127.0.0.1:8000/cuenta/registrar