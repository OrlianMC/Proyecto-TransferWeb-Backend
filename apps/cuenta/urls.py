from django.urls import path, include
from apps.cuenta.views import cuenta_registrar

urlpatterns = [
    path('registrar/', cuenta_registrar, name='usuarios-registrar'),
]

#http://127.0.0.1:8000/cuenta/