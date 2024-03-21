from django.urls import path
from apps.servicio.views import *

urlpatterns = [
    path('gestionar/', gestionar_servicio, name='servicio-gestionar'),
]
