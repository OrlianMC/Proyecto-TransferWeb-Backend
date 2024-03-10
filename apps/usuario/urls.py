from django.urls import path, include
from apps.usuario.views import *
# from transfermovil_app.api.login import buscar_usuario

urlpatterns = [
    path('registrar/', perfil_registrar, name='usuarios-registrar'),
    path('modificar/', perfil_administrar, name='usuarios-modificar'),
    path('formulario/', perfil_formulario, name='cargar-usuario-formulario'), #Devuelve datos de usuario para llenar formulario de modificar
    path('login/', login_user, name='login-user'),#Login
    path('logout/', logout_user, name='logout-user'),#Logout
]

#http://127.0.0.1:8000/usuario/login/