from django.urls import path
from apps.cuenta.views import *

urlpatterns = [
    path('gestionar/', cuenta_gestionar, name='cuenta_gestionar'),
    path('formulario/', cuenta_formulario, name='cuenta-formulario'),
]

#http://127.0.0.1:8000/cuenta/registrar